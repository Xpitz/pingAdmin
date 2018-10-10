
$(window).on('load', function() {
	// Pagination
	// -----------------------------------------------------------------
    var $pagination = $('#foo_pagination'),
    $showEntries = $('#foo_show_entries'),
    $search = $('#foo_search');
	$pagination.footable();
	$showEntries.change(function (e) {
		e.preventDefault();
		var pageSize = $(this).val();
		$pagination.data('page-size', pageSize);
		$pagination.trigger('footable_initialized');
	});

	// Search input
	$search.on('input', function (e) {
		e.preventDefault();
		$pagination.trigger('footable_filter', {filter: $(this).val()});
	});
});
