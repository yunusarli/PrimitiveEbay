from django.contrib.auth import authenticate, login, logout,get_user_model,get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .models import User, Listing, Bid, Comment
from django.views.generic import DeleteView
from django.core.exceptions import PermissionDenied

#a function return all bids list with desired name
def bid_list(title):

    bids = Bid.objects.all()
    bids_list = []
    for bid in bids:
        if bid.title == title:
            bids_list.append(bid)
    return bids_list

def index(request):

    user = get_user(request)
    products = Listing.objects.all()
    return render(request, "auctions/index.html",{
        'products':products,
        'user':user,
    })


def login_view(request):

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):

    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:

        return render(request, "auctions/register.html")


def create_listing(request):

    user = get_user(request)

    is_auth = authenticate(username=user.username,password=user.password)

    if request.method=="POST":
        #take all of the informations about listing
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        link = request.POST['link']
        category = request.POST['category']

        if name and description:
            
            listing = Listing(
                createdby=get_user(request),
                title=name,
                description=description,
                price=price,
                link=link,
                category=category,
                )
            listing.save()
            return redirect(index)
            
        else:
            return render(request,'auctions/create_listing.html',{
                'message':"you have to fill all of the inputs"
            })
    return render(request,'auctions/create_listing.html')



def detail_view(request,pk):

    """ 
        Showing all details about product and comments on the product. There is Four button.
        First one is for giving a bid.
        Second one is for viewing all bids.
        Third one is for adding product to watchlist.
        The last one is for leave a comment.
    """
    product_detail = Listing.objects.get(id=pk)

    title = product_detail.title
    
    if request.method == 'POST':

        

        if 'newbid' in request.POST:

            #update the current price
            bid = request.POST.get('bid',False)
            for bids in bid_list(title):
                if int(bids.price)>=int(bid):
                    return render(request,'auctions/detail.html',{
                                'object':product_detail,
                                'message':"you have to bid higher than existing bids",
                            })

            product_detail.price = bid

            product_detail.save()
            #Create a new bid
            user = get_user(request)
            create_bid = Bid(user=user,title=title,price=bid)
            create_bid.save()
            
        elif 'watchlist' in request.POST:
            #add to watchlist
            return HttpResponse('hello world')

        elif 'allbids' in request.POST:
            #showing up the all bids
            return render(request,'auctions/allbids.html',{
                'bids_list':bid_list(title),
            })



    return render(request,'auctions/detail.html',{

        'object':product_detail,
        

    })


class ListingDeleteView(DeleteView):
    """ a django class-based view to delete the post. """
    model = Listing
    template_name = 'auctions/delete.html' 
    success_url = reverse_lazy('index')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        """ 
            This function allows us to disallow users without permission  
        """

        obj = self.get_object()

        if not obj.createdby == self.request.user:
            raise PermissionDenied
            
        return super().dispatch(request, *args, **kwargs)

#To Do: comments, WatchList, Categories, Images on database.