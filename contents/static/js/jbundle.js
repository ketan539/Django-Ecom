// $(document).ready(function () {
//     $(".form-check-input,#pricefilter_btn").on('click', function () {

//         var _filterObj = {}
//         var _minPrice =$('#maxPrice').attr('min')
//         var _maxPrice =$('#maxPrice').val();
//         _filterObj._minPrice=_minPrice;
//         _filterObj.maxPrice=_maxPrice;
//         $(".form-check-input").each(function (index, ele) {
//             var _filterVal = $(this).val();
//             var _filterKey = $(this).data('filter');
//             _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter=' + _filterKey + ']:checked')).map(function () {
//                 return ele.value;
//             });
//         });
//         $.ajax({
//                 url:'/filter-data',
//                 data:filters,
//                 dataType:'json',
//                 beforeSend:function(){
//                 $("#filteredProducts").html('Loading..');
//                 },
//                 success:function(res){
//                 $('#filteredProducts').html(res.data)
//                 console.log(res);
//                          }
//                      })
//     });

// });
// $(function() {
//     const $priceFilterBtn = $('#pricefilter_btn');
//     const $maxPrice = $('#maxPrice');
//     const minPrice = $maxPrice.prop('min');

//     $priceFilterBtn.on('click', function() {
//       const _filterObj = {
//         _minPrice: minPrice,
//         maxPrice: $maxPrice.val()
//       };

//       $('.form-check-input').each(function(index, ele) {
//         const $this = $(this);
//         const filterVal = $this.val();
//         const filterKey = $this.data('filter');
//         const checkedInputs = $(`input[data-filter=${filterKey}]:checked`).map(function() {
//           return this.value;
//         }).get();
//         _filterObj[filterKey] = checkedInputs;
//       });
//     });
//   });
$(document).ready(function () {
    const filters = {};
    $(".form-check-input,#pricefilter_btn").on('change', function () {
        const filterKey = $(this).data('filter');
        const filterVal = $(this).val();
        const minPrice = $('#maxPrice').attr('min');
        const maxPrice = $('#maxPrice').val();
        filters.minPrice = minPrice;
        filters.maxPrice = maxPrice;
        if (!filters[filterKey]) {
            filters[filterKey] = [];
        }
        if ($(this).is(':checked')) {
            filters[filterKey].push(filterVal);
        } else {
            filters[filterKey] = filters[filterKey].filter(v => v !== filterVal);
        }
        $.ajax({
            url: '/filter-data',
            data: filters,
            dataType: 'json',
            beforeSend: function () {
                $("#filteredProducts").html('Loading..');
            },
            success: function (res) {
                $('#filteredProducts').html(res.data)
                console.log(res);
            }
        })
    });

});

$(document).ready(function () {

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


})








