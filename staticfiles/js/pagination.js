// $(document).ready(function () {
//     $('#loadmore').on('click',function(){
//         var _currentProducts=$(".product-box").length;
//         var _limit=$(this).attr('data-limit');
//         var _total=$(this).attr('data-total');
//         console.log(_currentProducts,_limit,_total);

//     })
//     $.ajax({
//         url: '/load-more-data',
//         data: {
//             limit: _limit,
//             offset:_currentProducts

//         },
//         dataType: 'json',
//         beforeSend: function () {
//             $("#loadmore").attr('disabled',true);
//             $(".spinner").addClass('fa-spin')
//         },
//         success: function (res) {
//             $("#filteredProducts").append(res.data);
//             $("#loadmore").attr('disabled',false);
//             $(".spinner").removeClass('fa-spin')
//         }
//     })


// });

// $(document).ready(function () {
//     let _currentProducts = $(".product-box").length;
//     let _limit = $('#loadmore').attr('data-limit');
//     let _total = $('#loadmore').attr('data-total');

//     $('#loadmore').on('click', function () {
//       $.ajax({
//         url: '/load-more-data',
//         data: {
//           limit: _limit,
//           offset: _currentProducts
//         },
//         dataType: 'json',
//         beforeSend: function () {
//           $("#loadmore").attr('disabled', true);
//           $(".spinner").addClass('fa-spin');
//         },
//         success: function (res) {
//           $("#filteredProducts").append(res.data);
//           _currentProducts = $(".product-box").length;
//           $("#loadmore").attr('disabled', false);
//           $(".spinner").removeClass('fa-spin');

//           let _totalShowing = $(".product-box").length
//           if(_totalShowing == _total){
//             $("#loadmore").remove();
//         }

//        }

//       });
//     });
//   });


$(document).ready(function () {
    const $loadmore = $('#loadmore');
    const $filteredProducts = $('#filteredProducts');
    const $spinner = $('.spinner');
    const _currentProducts = $(".product-box").length;
    const _limit = $loadmore.attr('data-limit');
    const _total = $loadmore.attr('data-total');

    $loadmore.on('click', function () {
        $.ajax({
            url: '/load-more-data',
            data: {
                limit: _limit,
                offset: _currentProducts
            },
            dataType: 'json',
            beforeSend: function () {
                $loadmore.attr('disabled', true);
                $spinner.addClass('fa-spin');
            },
            success: function (res) {
                $filteredProducts.append(res.data);
                const _totalShowing = $(".product-box").length
                if (_totalShowing == _total) {
                    $loadmore.remove();
                } else {
                    $loadmore.attr('disabled', false);
                }
                $spinner.removeClass('fa-spin');
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
    });

    // Variation         
    $('.choose_size').hide();

    //Show Storage according to color
    $('.choose_color').on('click', function () {
        $('.choose_size').removeClass('focused')
        $(this).addClass('focused')

        let _color = $(this).attr('data-color');
        $('.choose_size').hide();
        $('.color' + _color).show();
        $('.color' + _color).first().addClass('active');

        let _price = $('.choose_size').first().attr('data-price');
        $('.product-price').text(_price)

    })
    //Show price according to selected color and size

    $('.choose_size').on('click', function () {
        $('.choose_size').removeClass('active')
        $(this).addClass('active')


        let _price = $(this).attr('data-price');
        $('.product-price').text(_price)
    })

    // Show first selected color
    $('.choose_color').first().addClass('focused')
    let _color = $('.choose_color').first().attr('data-color');
    let _price = $('.choose_size').first().attr('data-price');

    $('.color' + _color).show();
    $('.color' + _color).first().addClass('active');
    $('.product-price').text(_price)

    // Add to cart
    $(document).on('click', '.addcart_btn', function () {
        let _cart = $(this);
        let _index = _cart.attr('data-index');
        let _product_qty = $('.product_qty-' + _index).val();
        let _product_id = $('.product_id-' + _index).val();
        let _product_title = $('.product_title-' + _index).val();
        let _product_price = $('.product-price-' + _index).text();
        let _product_image = $('.product_image-' + _index).val();

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': _product_id,
                'qty': _product_qty,
                'title': _product_title,
                'price': _product_price,
                'image': _product_image

            },
            dataType: 'json',
            beforeSend: function () {
                _cart.attr('disabled', true);
            },
            success: function (res) {
                $('#cart-list').text(res.totalitems);
                _cart.attr('disabled', false);
            },
            error: function (xhr, status, error) {
                console.error(error);
            }


        })
    });
    //Delete from cart
    $(document).on('click', '.delete_item', function () {
        let _product_id = $(this).attr('data-item');
        let _cart = $(this);
        $.ajax({
            url: '/delete-from-cart',
            data: {
                'id': _product_id,
            },
            dataType: 'json',
            beforeSend: function () {
                _cart.attr('disabled', true);
            },
            success: function (res) {
                $('#cart-list').text(res.totalitems);
                _cart.attr('disabled', false);
                $('#cart_item').html(res.data)
            },
        })
    });
    // Update from cart
    $(document).on('click', '.update_item', function () {
        let _product_id = $(this).attr('data-item');
        let _product_qty = $('.product_qty-' + _product_id).val();
        let _cart = $(this);
        $.ajax({
            url: '/update_from_cart',
            data: {
                'id': _product_id,
                'qty': _product_qty
            },
            dataType: 'json',
            beforeSend: function () {
                _cart.attr('disabled', true);
            },
            success: function (res) {
                // $('#cart-list').text(res.totalitems);
                _cart.attr('disabled', false);
                $('#cart_item').html(res.data)
            },
        })
    });

    $(document).ready(function () {
        $('#addform').submit(function (e) {
            $.ajax({
                data: $(this).serialize(),
                method: $(this).attr('method'),
                url: $(this).attr('action'),
                dataType: 'json',
                success: function (res) {
                    if (res.bool == true) {
                        $('#ajaxRes').html('Data has been saved');
                        $('#reset').trigger('click');
                        $('.reviewBtn').hide();
                        $('#reviewbtn').modal('hide');

                        var _html = '<blockquote class="blockquote text-right">';
                        _html += '<small>' + res.data.review_text + '</small>';
                        _html += '<footer class="blackquote-footer">' + res.data.user;
                        _html += '<cite title="Source Title">';
                        for (var i = 1; i <= res.review_rating; i++) {
                            _html += '<i class="fa fa-star text-warning"></i>';
                        }
                        _html += ' </cite>';
                        _html += ' </footer>';
                        _html += ' </blockquote>';
                        _html += ' </hr>';


                        $('.review_list').prepend(_html);
                        $('.avg_rating').text(res.avg_rating.avg_rating.toFixed(1));
                    }
                }
            });
            e.preventDefault();
        });

        // Add to cart single-page
        $('.add-to-cart').on('click', function () {
            let _cart = $(this);
            let _index = _cart.attr('data-index');
            let _product_qty = $('#product_qty-' + _index).val();
            let _product_id = $('#product_id-' + _index).val();
            let _product_title = $('#product_title-' + _index).val();
            let _product_price = $('.product-price-' + _index).text();
            let _product_image = $('#product_image-' + _index).val();

            $.ajax({
                url: '/add-to-cart',
                data: {
                    'id': _product_id,
                    'qty': _product_qty,
                    'title': _product_title,
                    'price': _product_price,
                    'image': _product_image

                },
                dataType: 'json',
                beforeSend: function () {
                    _cart.attr('disabled', true);
                },
                success: function (res) {
                    $('#cart-list').text(res.totalitems);
                    _cart.attr('disabled', false);
                },
                error: function (xhr, status, error) {
                    console.error(error);
                }


            })
        });




        $('.add_wishlist').on('click', function () {
            let _pid = $(this).attr('data-product');
            let _wishlist = $(this);
            $.ajax({
                url: '/add_wishlist',
                data: {
                    product: _pid
                },
                dataType: 'json',
                success: function (res) {
                    if (res.bool == true) {
                        _wishlist.addClass('disabled').removeClass('add_wishlist')

                    }
                    console.log(res)
                }
            })


        });

        $(document).on('click', '.activate_address', function () {
            let _aid = $(this).attr('data-address')
            let _vm = $(this);
            //Ajax
            $.ajax({
                url: '/activate_address',
                data: {
                    'id': _aid,
                },
                dataType: 'json',
                success: function (res) {
                  if (res.bool==true){
                    $('.address').removeClass('border-info shadow');
                    $('.address'+_aid).addClass('border-info shadow');

                    $('.check').hide();
                    $('.actbtn').show();
                    
                    $('.check'+_aid).show();
                    $('.btn'+_aid).hide();

                  }
                }
            });
        });
    });
});





