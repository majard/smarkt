const SUCCESS_MESSAGE_DURATION = 1111;
const ERROR_MESSAGE_DURATION = 3000;
const REDIRECT_DELAY = 1200;
const FADE_IN_ANIMATION_TIMEOUT = 320;
const FADE_IN_ANIMATION_DURATION = 300;


$(document).ready(function() {
    // Create a product
    $(".create-product").click(function(e){
        $(this).prop('disabled', true);
        
        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            }
        })
        
        e.preventDefault();

        var cnpj = $("input[name='cnpj']").val();

        var nome = $("input[name='nome']").val();        

        $.ajax({            
            
            url: "/cadastro/producta",

            type:'POST',

            data: {cnpj:cnpj, nome:nome},

            success: function(data) {                  

                $('.errorNome').addClass('hidden');
                $('.errorCnpj').addClass('hidden');

                toastr.success('A clínica foi cadastrada com sucesso!', 'Sucesso!', {timeOut: SUCCESS_MESSAGE_DURATION});
                setTimeout(function(){
                    location.href='/productas';
                }, REDIRECT_DELAY);
            },
            
            error: function(data){
                $('.create-product').prop('disabled', false);
                var errors = data.responseJSON.errors;

                if (errors){
                    toastr.error('Erro de Validação!', 'Erro!', {timeOut: ERROR_MESSAGE_DURATION});

                    var errors = data.responseJSON.errors;
                    
                    // Render the errors with js ...
                    if (errors.nome) {
                        $('.errorNome').removeClass('hidden');
                        $('.errorNome').text(errors.nome);
                    }
                    if (errors.cnpj) {
                        $('.errorCnpj').removeClass('hidden');
                        $('.errorCnpj').text(errors.cnpj);
                    }
                } 
                else {
                    toastr.error(data.responseJSON.message, 'Erro!', {timeOut: ERROR_MESSAGE_DURATION});
                }
            }
        });
    }); 

    // Open edit modal
    $(document).on('click', '.product.edit-modal', function() {
        $('.product.edit').prop('disabled', false);
        $('.modal-title').text('Edit');
        $('#nome_edit').val($('#nome').text());
        $('#cnpj_edit').val($('#cnpj').text());
        id = $(this).val();
        $('#editModal').modal('show');
    });
    
    // Edit a product
    $('.modal-footer').on('click', '.product.edit', function() {
        $(this).prop('disabled', true);

        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            }
        })

        $.ajax({
            
            type: 'PUT',
            url: '/productas/' + id,
            data: {
                'id': id,
                'nome': $('#nome_edit').val(),
                'cnpj': $('#cnpj_edit').val()
            },

            success: function(data) {          
                $('.errorNome').addClass('hidden');
                $('.errorCnpj').addClass('hidden');
                $('#editModal').modal('hide');
                $('#nome').text(data.nome);       
                $('#cnpj').text(data.cnpj);
                $('#nome').val(data.nome);
                $('#cnpj').val(data.cnpj);

                toastr.success('A edição foi feita com sucesso!', 'Successo!', {timeOut: SUCCESS_MESSAGE_DURATION});                    
            },
            
            error: function(data){                                
                $('.product.edit').prop('disabled', false);
                var errors = data.responseJSON.errors;

                if (errors){
                    toastr.error('Erro de Validação!', 'Erro!', {timeOut: ERROR_MESSAGE_DURATION});

                    // Render the errors with js
                    if (errors.nome) {
                        $('.errorNome').removeClass('hidden');
                        $('.errorNome').text(errors.nome);
                    }
                    if (errors.cnpj) {
                        $('.errorCnpj').removeClass('hidden');
                        $('.errorCnpj').text(errors.cnpj);
                    }
                } 
                else if (data.status == 403){
                    toastr.error('Você não pode editar essa producta!', 'Erro!', {timeOut: ERROR_MESSAGE_DURATION});
                }
                else if (data.status == 409){
                    toastr.error('Já existe uma producta com esse cnpj!', 'Erro!', {timeOut: ERROR_MESSAGE_DURATION});
}
                else 
                {
                    toastr.error(data.responseJSON.message, 'Erro!', {timeOut: ERROR_MESSAGE_DURATION});
                }
            }
        });
    });

    // Open delete modal
