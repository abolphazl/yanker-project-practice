


$(".carrier").click(function() {
	let episode_id = $(this).attr("episode_id")
	$("#episode-id").val(episode_id);
	$(".close-modal").attr("href", "#" + episode_id);
})