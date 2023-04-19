from flask import flash, redirect, render_template, request, url_for
from app import app
from .forms import PostForm
from .models import Like, Post, User
from flask_login import  current_user, login_user, logout_user, login_required

@app.route('/')
def homePage():
    users = User.query.all()
    

    return render_template('index.html', users=users)



@app.route('/posts/create', methods=['GET', "POST"])
@login_required
def createPost():
    form = PostForm()
    if request.method == 'POST':
        if form.validate():
            #create post and save to db
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post = Post(title, img_url, caption, current_user.id)

            post.saveToDB()

            return redirect(url_for('showAllPosts'))
    return render_template('createpost.html', form = form)

@app.route('/posts')
def showAllPosts():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('posts.html', posts = posts)

@app.route('/posts/<int:post_id>')
def showPost(post_id):
    post = Post.query.get(post_id)
    if post:
        return render_template('singlepost.html', post = post)
    else:
        return redirect(url_for('showAllPosts'))
    
@app.route('/posts/delete/<int:post_id>')
@login_required
def deletePost(post_id):
    post = Post.query.get(post_id)
    if post:
        if post.user_id == current_user.id:
            post.deleteFromDB()
        else:
            flash("You cannot delete another user's post.", 'danger')
    else:
        flash("The post you are trying to delete does not exist.", 'danger')
    return redirect(url_for('showAllPosts'))


@app.route('/posts/update/<int:post_id>', methods = ['GET', 'POST'])
@login_required
def updatePost(post_id):
    post = Post.query.get(post_id)
    if post:
        if post.user_id == current_user.id:
            form = PostForm()
            if request.method == "POST":
                if form.validate():
                    title = form.title.data
                    img_url = form.img_url.data
                    caption = form.caption.data
                    
                    post.title = title
                    post.img_url = img_url
                    post.caption = caption

                    post.saveChangesToDB()
                    flash('Succesfully updated your post!', 'success')
                    return redirect(url_for('showPost', post_id=post.id))
                    
            return render_template('updatepost.html', form = form, post = post)
        else:
            flash("You cannot update another user's post.", 'danger')
    else:
        flash('The post you are trying to update does not exist', 'danger')
    return redirect(url_for('showAllPosts'))

@app.route('/posts/like/<int:post_id>')
@login_required
def likePost(post_id):
    like = Like(current_user.id, post_id)
    like.saveToDB() 
    return redirect(url_for('showAllPosts'))

@app.route('/posts/unlike/<int:post_id>')
@login_required
def unlikePost(post_id):
    like = Like.query.filter_by(post_id=post_id).first()
    if like:
        like.deleteFromDB()
    return redirect(url_for('showAllPosts'))

@app.route('/follow/<int:user_id>')
@login_required
def followUser(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.follow(user)
    return redirect(url_for('homePage'))

@app.route('/unfollow/<int:user_id>')
@login_required
def unfollowUser(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.unfollow(user)
    return redirect(url_for('homePage'))