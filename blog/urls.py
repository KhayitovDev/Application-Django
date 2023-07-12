from django.urls import path
from .views import ( PostListView, PostDetailView,
                     CommentCreateView, CreateUserView,
                       UserLogin, UserLogout,PostCreateView, 
                       DraftPostsListView, DraftPostDetailView, PostUpdate, CategoryListView, 
                       CategoryCreateView, CommentListView,
                        PostDeleteView, CommentUpdate, 
                        CommentReplyView, MostCommented, MostLiked )

urlpatterns = [

    #user authentication urls
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    #--------------------------------------------------------#
    #post urls
    path('', PostListView.as_view(), name='home_page'),
    path('post_detail/<int:pk>', PostDetailView.as_view(), name='detail'), 
    path('create_post/', PostCreateView.as_view(), name='create_post'),
    path('post_update/<int:pk>/', PostUpdate.as_view(), name='update'),
    path('post_delete/<int:pk>/', PostDeleteView.as_view(), name='delete'),
    path('most_commented/',MostCommented.as_view(), name='most_commented_posts' ),
    path('most_liked/', MostLiked.as_view(), name='most_liked'),
    path('post_detail/<int:pk>/', PostDetailView.as_view(), name='likes'),
    #-------------------------------------------------------#

    #draft posts urls
    path('drafts/', DraftPostsListView.as_view(), name='draft_posts'),
    path('drafts/<int:pk>/', DraftPostDetailView.as_view(), name='draft_detail'),
    #-----------------------------------------------------#

    #comment urls
    path("comments/<int:pk>/", CommentListView.as_view(), name="comment_detail"),
    path('post_detail/<int:pk>/create-comment/', CommentCreateView.as_view(), name='comment_create'),
    path('comment_update/<int:pk>/', CommentUpdate.as_view(), name='update_comment'),
    path('comments/<int:pk>/reply_to_comment/', CommentReplyView.as_view(), name='reply_to_comment'),

    #------------------------------------------------------#
    #category urls
    path('category/', CategoryListView.as_view(), name='category'),
    path('create_category/', CategoryCreateView.as_view(), name='create_category'),

   
]