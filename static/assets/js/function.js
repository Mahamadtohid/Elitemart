console.log("Working.......................................")
const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

$("#commentForm").submit( function(e){
    e.preventDefault();

    let date = new Date()
    let time = date.getDay() + " " + months[date.getUTCMonth] + " ," + date.getUTCFullYear()

    $.ajax({
        data : $(this).serialize(),


        method : $(this).attr("method"),

        url : $(this).attr("action"),
        datatype : "json",

        success : function(response){
            console.log("Comment saved in DB....");

            if(response.bool == true){
                $("#review-res").html("Review added successfully")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html +='<div class="thumb text-center">'
                    _html +='<img src = https://imgs.search.brave.com/olU1frCI_rKOD3-NBWDPcqTpdn8YDMNYb2wVQ2TmqlM/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzAzLzQ2LzgzLzk2/LzM2MF9GXzM0Njgz/OTY4M182bkFQemJo/cFNrSXBiOHBtQXd1/ZmtDN2M1ZUQ3d1l3/cy5qcGc" alt="" />'
                    _html +='<a href="#" class="font-heading text-brand">'+ response.context.user+'</a>'
                    _html +='</div>'

                    _html +='<div class="desc">'
                    _html +='<div class="d-flex justify-content-between mb-10">'
                    _html +='<div class="d-flex align-items-center">'
                    _html +='<span class="font-xs text-muted">'+ time +'</span>'
                    _html +='</div>'

                    _html +='<div class="product-rate d-inline-block">'
                    _html +='<div class="product-rating" style="width: 100%"></div>'
                    _html +='</div>'
                    for(var i= 1; i<=response.context.rating ;i++){
                        _html +='<i class="fas fa-star text-warning"></i>'
                    }
                    _html +='</div>'
                    _html +='<p class="mb-10">'+ response.context.review +'</p>'

                    _html +='</div>'
                    _html +='</div>'
                    _html +='</div>'

                    $(".comment-list").prepend(_html)
                }
                
            
        }
    })

})



$(document).ready( function(){
    $(".filter-checkbox, #price-filter-btn").on("click" , function(){
        console.log("Checkbox clicked"); 
        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price
        filter_object.max_price = max_price

        // let filter_object = {}
        $(".filter-checkbox").each(function(index){
            let filter_value = $(this).val()

            let filter_key = $(this).data("filter")

            console.log("filter value is" , filter_value)
            console.log("filter key is" , filter_key)
            // console.log(filter_value , filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter = '+ filter_key+' ]:checked')).map(function(element){

                return element.value
            })
            
        })
        console.log(filter_object)
        $.ajax({
            url: '/filter-products',
            data : filter_object,
            datatype : 'json',
            beforeSend : function(){
                console.log("Sending data....");
            },
            success : function(response){
                    
                    console.log(response);
                    console.log("data send successfully.......")
                    $("#filtered-product").html(response.data)

                }
        })

    })

    $("#max_price").on("blur" ,function(){

        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()


        min_price = (min_price * 100)/100
        max_price = (max_price * 100)/100
        current_price =(current_price * 100)/100

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            console.log("invalid price")
            // min_price = Math.round(min_price * 100)/100

            alert("Price must be between ₹" + min_price  + ' and ₹' + max_price)
            $(this).val(min_price)
            $("#range").val(min_price)
            $(this).focus()
            
            return false
    }
    })



    $(".add-to-cart-btn ").on("click",  function(){
        let this_val = $(this)
        let index =  this_val.attr("data-index")
    
        let quantity = $(".product-quantity-"+ index).val()
        let product_title = $(".product-title-"+ index).val()
    
        let product_id = $(".product-id-"+ index).val()
        let product_price = $(".current-product-price"+ index).text()
        let product_image = $(".product-image-"+ index).val()
    
        let product_productid = $(".product-pid-"+ index).val()
        
    
    
        console.log(" quantity", quantity)
        console.log(" title",product_title)
        console.log(" ID",product_id)
        console.log(" image",product_image)
        console.log(" productid",product_productid)
        console.log(" price",product_price)
        console.log(" index",index)
        console.log("Current Elemet" , this_val)
    
        $.ajax({
            url: '/add-to-cart',
            data : {
                'id' : product_id,
                'pid':product_productid,
                'image': product_image,
                'quantity':quantity,
                'title':product_title,
                'price':product_price
    
            },
            datatype:'json',
            beforeSend : function(){
                console.log("Adding products to cart..................");
                
    
            },
            success : function(response){
                this_val.html("✓")
                console.log("Addeng products to cart..................");
                $(".cart-items-count").text(response.total)
    
            }
        })
    
    
        
    
    }) 
    
    
    $(".delete-product").on("click",  function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("product_id : " , product_id);

        $.ajax({
            url : "/delete-from-cart",
            data:{
                "id":product_id
            },
            dataType: "json",
            beforeSend:function(){
                this_val.hide()
            },
            success:function(response){
                this_val.show()
                $(".cart-items-count").text(response.total)
                $("#cart-list").html(response.data)
            }
        })
    })



    $(".update-product").on("click",  function(){
    
        let product_id = $(this).attr("data-product")
        let product_quantity = $(".product-quantity-"+product_id).val()
        let this_val = $(this)
    
        console.log("product_id : " , product_id);
        console.log("product_qty : " , product_quantity);

        $.ajax({
            url : "/update-cart",
            data:{
                "id":product_id,
                "quantity":product_quantity,
            },
            dataType: "json",
            beforeSend:function(){
                this_val.hide()
            },
            success:function(response){
                this_val.show()
                $(".cart-items-count").text(response.total)
                $("#cart-list").html(response.data)
            }
        })
    })



    //Making default Address

    $(document).on("click" , ".make-default-address" , function(){
        let id= $(this).attr("data-address-id")

        let this_val = $(this)

        console.log(id)
        console.log(this_val)
        $.ajax({
            url:'/make-default-address',
            data:{
                'id':id,

            },
            dataType:"json",
            success:function(response){
                console.log("Success")
                if(response.boolean == true){
                    
                    $(".check").hide()
                    $(".action_btn").show()


                    $(".check" + id).show()
                    $(".button" + id).hide()

                }
            }
        })
    })
})



// Add to cart




