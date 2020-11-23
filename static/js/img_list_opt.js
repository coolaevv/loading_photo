$( document ).ready(function(){

    $('.edit').click(function(){
        let el = $(this).parents('.img-block').attr('id')
        $(this).hide()
        $(this).siblings('.ok').fadeIn()
        let val_h1 = $('#' + el).children('h1').text()
        $('#' + el).children('h1').replaceWith('<textarea class="edit_h1">' + val_h1 + '</textarea>')
        let val_p = $('#' + el).children('p').text()
        $('#' + el).children('p').replaceWith('<textarea class="edit_p">' + val_p + '</textarea>')

        $('.ok').click(function(){
            let a = $('#' + el).children('.edit_h1').val()
            let b = $('#' + el).children('.edit_p').val()

            $('#' + el).children('.edit_h1').replaceWith('<h1>' + a + '</h1>')
            $('#' + el).children('.edit_p').replaceWith('<p>' + b + '</p>')

            $(this).hide()
            $(this).siblings('.edit').fadeIn()

            let d_id = $(this).parents('.img-block').attr('id')

            if(typeof a != false && typeof b != 'undefined'){
                $.ajax({
                    type: 'post',
                    url: '/edit_data',
                    data: {'id': d_id, 'title': a, 'desc': b},
                    success: function(data){
                        console.log(data)
                    },
                    error: function(error) {
                        console.log(error);
                    }
                })
            }
        })
    })

    $('.del').click(function(){
        let el = $(this).parents('.img-block').attr('id')
        $.ajax({
            type: 'post',
            url: '/del_data',
            data: {'id': el},
            success: function(data){
                console.log(data)
            },
            error: function(){
                console.log('error')
            }
        })
        $(this).parents('.img-block').fadeOut(500)
    })

})