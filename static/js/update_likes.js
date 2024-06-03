function updateLikeIcon(event, messageId) {
    var response = event.detail.xhr.response;
    var data = JSON.parse(response);
    var icon = document.getElementById('like-icon-' + messageId);
    var likeCount = document.getElementById('like-count-' + messageId);

    if (data.is_liked) {
        icon.classList.remove('fa-regular');
        icon.classList.add('fa-solid');
        icon.style.color = '#ef1c5c';
    } else {
        icon.classList.remove('fa-solid');
        icon.classList.add('fa-regular');
        icon.style.color = '#687684';
    }

    likeCount.textContent = data.like_count;
}