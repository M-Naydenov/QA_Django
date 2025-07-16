var search_btn = (document.querySelector(".search_btn"));
var search_close_btn = (document.querySelector(".search_close_btn"));
var input_search = (document.querySelector(".input_search"));
var search_box_wrap = (document.querySelector(".search-box-wrap"));

search_btn.addEventListener("click", function(){
    search_box_wrap.classList.add("active");
    }
)
search_close_btn.addEventListener("click", function(){
    search_box_wrap.classList.remove("active");
    }
)
