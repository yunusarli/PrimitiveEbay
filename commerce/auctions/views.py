from django.contrib.auth import authenticate, login, logout,get_user_model,get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .models import User, Listing, Bid, Comment, WatchLists
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='login')
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
        image = request.FILES['img']
        if name and description:
            
            listing = Listing(
                createdby=get_user(request),
                title=name,
                description=description,
                price=price,
                link=link,
                category=category,
                image=image,
                )
            listing.save()
            return HttpResponseRedirect(reverse('index'))
            
        else:
            return render(request,'auctions/create_listing.html',{
                'message':"you have to fill all of the inputs"
            })
    return render(request,'auctions/create_listing.html')


@login_required(login_url='login')
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
    user = get_user(request)
    
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
            
            create_bid = Bid(user=user,title=title,price=bid)
            create_bid.save()
            
        elif 'watchlist' in request.POST:
            if WatchLists.objects.filter(user = get_user(request),items=pk).exists():
                return HttpResponseRedirect(reverse('watchlist'))
            
            user_list, created = WatchLists.objects.get_or_create(user=get_user(request))
            user_list.items.add(product_detail)

            return HttpResponseRedirect(reverse('watchlist'))

        elif 'remove' in request.POST:

            if WatchLists.objects.filter(user = get_user(request),items=pk).exists():
                user_list, created = WatchLists.objects.get_or_create(user=get_user(request))
                user_list.items.remove(product_detail)
                return HttpResponseRedirect(reverse('watchlist'))
            else:
                return render(request,'auctions/watchlist.html',{
                    'message':"Sorry this item doesnt exist",
                })
            
            

            


        elif 'allbids' in request.POST:
            #showing up the all bids
            return render(request,'auctions/allbids.html',{
                'bids_list':bid_list(title),
            })
        elif 'leave_a_comment' in request.POST:
            cmmnt = request.POST['comment']
            create_comment = Comment(title=product_detail,comment=cmmnt,author=user)
            create_comment.save()


    #To avoid multiple choises error, we used filter rather than the get() method.
    comments = Comment.objects.filter(title=pk)
    winner = ""
    max_bid = 0
    if not product_detail.isopen:

        all_bids = bid_list(title)
        hiddenbids = [0]

        for bid in all_bids:
            hiddenbids.append(int(bid.price))
        for k in all_bids:
            if hiddenbids[-1]==int(bid.price):
                winner = bid.user
        max_bid = sorted(hiddenbids)[-1]

    
    return render(request,'auctions/detail.html',{

        'object':product_detail,
        'comments':comments,
        'isopen':product_detail.isopen,
        'max_bid':max_bid,
        'winner':winner,
    })

@login_required(login_url='login')
def delete_view(request,pk):
    if request.method=='POST':
        object_ = Listing.objects.get(id=pk)
        object_.isopen = False
        object_.save()
        return HttpResponseRedirect(reverse('index'))

    return render(request,'auctions/delete.html',{
        'object':Listing.objects.get(id=pk),
    })

@login_required(login_url='login')
def categories(request):
    listings = []
    for list_ in Listing.objects.all():
        if not list_.category in listings:
            listings.append(list_.category)

    return render(request,'auctions/categories.html',{
                'category':listings,
            })

@login_required(login_url='login')
def orientation(request,slug):
    all_categories = []
    for list_ in Listing.objects.all():
        if list_.category==slug:
            all_categories.append(list_)

    return render(request,'auctions/view_categories.html',{
        'all_categories':all_categories,
    })

@login_required(login_url='login')
def watchlist(request):
    products = WatchLists.objects.filter(user=get_user(request))

    return render(request,"auctions/watchlist.html",{

        'products':products,
    })



