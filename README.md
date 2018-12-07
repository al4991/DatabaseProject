# PriCoSha
Web app using Flask and MySql for CS-3083 Intro to Databases at NYU Tandon.  
We are using Python 3, and are using pymysql to connect to our database.  
 
PriCoSha is a Flask app developed by Andrew Lucero (me c:), Carolyn Ann McCawley, and Cindy Lee.  
Our project has a public home page that will show content to users who are not logged in yet,   
offering the option to register and to log in. After a user logs in, the user is redirected to the home  
page. On the home page, both guests and users are able to view public posts within the last 24 hours.   
Users, however, can view all the posts that they created.   
Users who are logged in have the ability to view posts that are shared with them, as well as the ability  
to share posts, or tag other users in posts that public for them. When users are tagged in posts, they have  
the ability to either decline or accept the tag (or just leave it as pending) on the pending tags page.  
When a user tags another user in a post that is not public to the other user, an error is  
displayed on the index page.  
  
Users have the ability to post content. Text is mandatory, but there is the option to upload  
an image, as well as the option to mark posts to be public or private before posting. If a user   
has marked a post as private, after posting, there is the option to share the post with groups   
that user belongs to. Speaking of groups, users have the option to create groups of users to   
share content to. Users can add users to groups that they own.   
  
  
Additional features: 
- The ability to upload images in addition to text, and the ability to filter posts by content type    
  - Users can upload local images, and are able to press a simple button to    
    choose which types of posts they see  
- The ability to rate posts (with emojis of course)  
  - Users are able to rate posts with 6 different emojis. If the post is also a shared post,  
   upon going to the shared page, users are able to change their ratings there, which is also  
   reflected on the home page. The total amount of each rating is displayed for each post as well.       
- Removing groups, remove users from groups, as well as sever users  
  - Removing a user from a group does just that. Severing a user removes that user from all   
    groups you own, and removes you from all groups they own  

- Comments  
  - Users are able to comment on each post. Upon clicking the comment button for the post,  
    the user is redirected to another page, displaying the post and a list of current comments.   
    On that page, the user is able to submit a comment.   
   
 Contributions  
  - Andrew implemented comments, posting and sharing  
  - Cindy implemented ratings and the tagging system (including accepting, pending, and rejecting requests). 
  Cindy performed project testing and debugging. 
  - Carolyn implemented friendgroups and a number of related features (add/de friend, add/remove group)     
    as well as implementing the filtering feature AND writing the CSS.   
  - Login/Register was a group effort, as well as maintaining the Home page as we implemented   
    more and more features. 
  - Maintaining the html was also a group effort.
    
