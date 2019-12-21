function loadPosts(username) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if(this.readyState==4 && this.status==200){

        //document.getElementById("demo").innerHTML += this.responseText+"<p/> ";

        var html="";
        var posts=JSON.parse(JSON.parse( this.responseText));
        for (var i=0; i < posts.length; i++){
            html += "<li id=" + posts[i]['id'] + ">";
            html += "<h2>" + posts[i]['title']+"</h2>";
            if(posts[i]['photo']!=null){
                html += "<img src=\"\\media\\" + posts[i]['photo']+"\">";
            }
            html += "<p>" + posts[i]['content']+" </p>";
            html += "<p><b>" + posts[i]['author']+"</b> on "+posts[i]['date']+" </p>";

            if (posts[i]['author']==username ){
                 html += "<form action=\"/portfolio/post_delete/\" method=\"post\" class=\"message\" onsubmit=\"return confirm('Do you really want to delete post"+posts[i]['title']+"?');\">";
                 csrftoken = getCookie('csrftoken');
                 html += "<input type='hidden' name='csrfmiddlewaretoken' value='"+csrftoken+"'/><input type=\"\hidden\" name=\"post_id\" value=\""+posts[i]['id']+"\"><input type=\"submit\" value=\"Delete\"></form>";
            }
        }
        document.getElementById("posts").innerHTML += html;
    }
  };
  var postElems = document.getElementById("posts").getElementsByTagName("li");
  var minId=Number(postElems[postElems.length-1].id);
  //document.getElementById("demo").innerHTML += "</br>"+minId+"</br>"
  xhttp.open('GET', 'portfolio/post_view?lastPost='+minId, true);
  xhttp.send();
};
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};