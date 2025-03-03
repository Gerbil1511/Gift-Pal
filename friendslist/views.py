from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from friendslist.models import Friendship, FriendRequest  # Add this line
from planner.models import Planner
from wishlist.models import WishlistItem


@login_required
def send_friend_request(request, user_id):
    """
    Send a friend request to another user.
    """
    receiver = get_object_or_404(User, id=user_id)

    # Check for existing requests or friendships
    if FriendRequest.objects.filter(sender=request.user, receiver=receiver, status='pending').exists():
        messages.error(request, "Friend request already sent.")
    elif Friendship.objects.filter(user1=request.user, user2=receiver).exists() or \
        Friendship.objects.filter(user1=receiver, user2=request.user).exists():
        messages.error(request, "You are already friends.")
    else:
        try:
            FriendRequest.objects.create(sender=request.user, receiver=receiver)
            messages.success(request, "Friend request sent!")
        except ValidationError as e:
            messages.error(request, str(e))

    return redirect('friendslist:friendslist')


@login_required
def friend_requests(request):
    """
    Display pending friend requests, confirmed friends, and search results for the current user.
    """
    # Get the search query from the request
    search_query = request.GET.get('search_query', '').strip()
    search_results = []
    if search_query:
        # Filter users whose username contains the search query (excluding the current user and existing friends)
        confirmed_friends = Friendship.objects.filter(
            Q(user1=request.user) | Q(user2=request.user)
        )
        friend_ids = [request.user.id]  # Exclude the current user
        for friendship in confirmed_friends:
            if friendship.user1 == request.user:
                friend_ids.append(friendship.user2.id)
            else:
                friend_ids.append(friendship.user1.id)

        search_results = User.objects.filter(
            username__icontains=search_query
        ).exclude(id__in=friend_ids)

    # Fetch pending friend requests (either sent or received) for the current user
    pending_received_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
    pending_sent_requests = FriendRequest.objects.filter(sender=request.user, status='pending')


    # Fetch confirmed friends for the current user
    confirmed_friends = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )

    # Extract friends from confirmed_friends
    friends = []
    for friendship in confirmed_friends:
        if friendship.user1 == request.user:
            friends.append(friendship.user2)
        else:
            friends.append(friendship.user1)

    # Render the template with the search results and other data
    return render(request, 'friendslist/friendslist.html', {
        'pending_received_requests': pending_received_requests,
        'pending_sent_requests': pending_sent_requests,
        'friends': friends,
        'search_results': search_results,
        'search_query': search_query,
    })


@login_required
def accept_friend_request(request, request_id):
    """
    Accept a pending friend request and delete any redundant requests.
    """
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=request.user,
        status='pending'
    )
    try:
        # Create the friendship
        Friendship.objects.create(user1=request.user, user2=friend_request.sender)

        # Debug: Print the redundant requests before deleting them
        redundant_requests = FriendRequest.objects.filter(
            (Q(sender=request.user) & Q(receiver=friend_request.sender)) |
            (Q(sender=friend_request.sender) & Q(receiver=request.user))
        )
        print("Redundant requests to delete:", redundant_requests)  # Debug statement

        # Delete any pending friend requests between the two users (in either direction)
        redundant_requests.delete()

        messages.success(request, "Friend request accepted!")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect('friendslist:friendslist')


@login_required
def decline_friend_request(request, request_id):
    """
    Decline a pending friend request.
    """
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=request.user,
        status='pending'
    )
    try:
        friend_request.decline()
        messages.info(request, "Friend request declined.")
    except ValidationError as e:
        messages.error(request, str(e))

    return redirect('friend_requests')



@login_required
def friendsdetail(request, friend_id):
    """
    Display details of a specific friend.
    """
    friend = get_object_or_404(User, id=friend_id)

    # Fetch confirmed friends for the friend
    confirmed_friends = Friendship.objects.filter(
        Q(user1=friend) | Q(user2=friend)
    )

    # Extract friends from confirmed_friends
    friends_friends = []
    for friendship in confirmed_friends:
        if friendship.user1 == friend:
            friends_friends.append(friendship.user2)
        else:
            friends_friends.append(friendship.user1)

    events = Planner.objects.filter(user=friend)
    wishlist_items = WishlistItem.objects.filter(user=friend)


    return render(request, 'friendslist/frienddetail.html', {
        'friend': friend,
        'friends_friends': friends_friends,
        'events': events,
        'wishlist_items': wishlist_items,
    })


@login_required
def remove_friend(request, friend_id):
    """
    Remove a friendship between the logged-in user and the specified friend.
    """
    friend = get_object_or_404(User, id=friend_id)

    # Delete both directions of the friendship
    Friendship.objects.filter(
        Q(user1=request.user, user2=friend) | Q(user1=friend, user2=request.user)
    ).delete()

    messages.success(request, f"You have removed {friend.username} from your friends.")

    # Fetch pending requests for the current user
    pending_requests = FriendRequest.objects.filter(
        receiver=request.user,
        status='pending'
    )

    return render(request, 'friendslist/friendslist.html', {
        'pending_requests': pending_requests,
    })