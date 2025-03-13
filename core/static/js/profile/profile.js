let commentclick=document.querySelectorAll(".commentclick");

let user_comment = document.querySelectorAll(".user_comment");


    user_comment.forEach(comment => {
        
        comment.style.display = "none";
    }); 

    commentclick.forEach((btn, index) => {
        btn.addEventListener("click", function () {
          
            usercomment(index);
        
        });
    });
    

    function usercomment(index){
    
        if (user_comment[index].style.display == "none"){
        
                user_comment[index].style.display = "block";
        }
        else{
            
            user_comment[index].style.display = "none";
        }
            
   

    
    };
    