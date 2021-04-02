window.onload=function(){
  payWithPaystack();
};
function payWithPaystack(){
  var handler = PaystackPop.setup({
    key: '{{public_key}}',
    email:'{{email}}',
    amount: {{total_cost}} *100,
    currency: "NGN",
    callback: function(response){

      alert('success. transaction ref is ' + response.reference);
      var referenceid = response.reference;
      $.ajax({
        type: 'GET',
        url: '/verify/' + referenceid,
        beforeSend: function () {
          console.log('Sending request');
          $('.alert').text('Sending request');
        },
        success: function (response) {
          if (response[3].status == success) {
            $('.alert').removeClass('alert-warning');
            $('.alert').addClass('alert-success');
            $('.alert').text('Transaction verified');
            console.log('Transaction verified');
            $('form').trigger('reset');
            } else {
              $('.alert').text('Transaction reference not found');
            }

          }
        }

      })
    },
    onClose: function(){
    alert('Transaction was not completed, window closed');
    }
  });
  handler.openIframe();
}