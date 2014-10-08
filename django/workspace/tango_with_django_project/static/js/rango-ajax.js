$(document).ready(
    
    function() {
        
        $('#likes').click(
            function(){
                var catid;
                catid = $(this).attr("data-catid");
                $.get(
                    '/rango/like_category/',
                    {category_id: catid},
                    function(data){
                        $('#like_count').html(data);
                        $('#likes').hide();
                    }
                );                
            }
        );
        
        $('#suggestion').keyup(
            function(){
                var query;
                query = $(this).val();
                
                $.get(
                    '/rango/suggest_category',
                    { suggestion : query },
                    function(data){
                        $('#cats').html(data);
                    }
                );
                
            }
        );
        
        $('.rango-add').click(
            function(){
                var catid = $(this).attr("data-catid");
                var pagetitle = $(this).attr("data-pagetitle");
                var pagelink = $(this).attr("data-pageurl");
                
                $.get(
                    '/rango/auto_add_page/',
                    {
                        category_id: catid,
                        page_title: pagetitle,
                        page_link: pagelink
                    },
                    function(data){
                        $('#pages').html(data);
                        $me.hide();
                    }
                );                
            }
        );
        
    }
    
);