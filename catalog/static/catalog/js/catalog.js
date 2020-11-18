$(function () {
  // alerts auto-close
  window.setTimeout(function () {
    $('.alert').alert('close');
  }, 3000);

  // pagination
  $('#js-load-more').on('submit', function () {
    const form = $(this);
    let page = $('#js-page');
    let startIndex = $('#js-index');
    $('#js-load-button').prop('disabled', true);
    $('#js-load-spinner').show();
    $.ajax({
      url: form.attr('action'),
      data: form.serialize(),
      type: form.attr('method'),
      dataType: 'json',
      success: function (data) {
        if (data.has_next) {
          page.val(+page.val() + 1);
          startIndex.val(data.start_index);
        } else {
          form.hide();
        }
        $('#js-search-append').append(data.search_html);
        $('#js-load-spinner').hide();
        $('#js-load-button').removeAttr('disabled');
      }
    });
    return false;
  });

  // google-save
  $('#js-search-append').on('submit', '.js-import', function () {
    const form = $(this);
    $.ajax({
      url: form.attr('action'),
      data: form.serialize(),
      type: form.attr('method'),
      dataType: 'json',
      success: function (data) {
        form.closest('tr').hide(1000);
      }
    });
    return false;
  });
});
