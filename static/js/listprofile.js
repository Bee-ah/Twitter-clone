document.addEventListener('DOMContentLoaded', () => {
    initializeProfileList();
});

document.body.addEventListener('htmx:afterSwap', (event) => {
    if (event.detail.target.id === 'conteudo') {
        initializeProfileList();
    }
});

function initializeProfileList() {
    console.log("Carregando list profiles");
    const profileListElement = document.getElementById('profile-list');
    const loadMoreButton = document.getElementById('load-more-btn');
    let nextPage = 1;

    if (profileListElement && loadMoreButton) {
        console.log('mesagem de list if');

        function hoverEffect(profileElement) {
            profileElement.onmousemove = (e) => {
                const x = e.pageX - e.target.offsetLeft;
                const y = e.pageY - e.target.offsetTop;
                e.target.style.setProperty('--x', `${x}px`);
                e.target.style.setProperty('--y', `${y}px`);
            }
        }

        function fetchProfiles() {
            fetch('/api/profiless/?page=' + nextPage)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    const profiles = data.results;

                    profiles.forEach(profile => {
                        const profileElement = document.createElement('div');
                        profileElement.classList.add('card', 'mb-3', 'lista');
                        profileElement.style.maxWidth = '70%';

                        const profileRow = document.createElement('div');
                        profileRow.classList.add('row', 'g-0');

                        const profileImageCol = document.createElement('div');
                        profileImageCol.classList.add('circle');

                        const profileImage = document.createElement('img');
                        profileImage.src = profile.profile_image || '/static/images/default.png';
                        profileImage.classList.add('imagem');
                        profileImage.width = 200;
                        profileImage.height = 200;
                        profileImageCol.appendChild(profileImage);

                        const profileInfoCol = document.createElement('div');
                        profileInfoCol.classList.add('col');

                        const profileCardBody = document.createElement('div');
                        profileCardBody.classList.add('card-body');

                        const profileTitle = document.createElement('h5');
                        profileTitle.classList.add('card-title');
                        profileTitle.textContent = profile.user.username;
                        console.log(profile.user.id);

                        const profileTitleMiddle = document.createElement('span');
                        profileTitleMiddle.innerHTML = '&#183;';

                        const profileLink = document.createElement('a');
                        var profileId = profile.user.id;
                        profileLink.href = `/profile/${profileId}`;
                        profileLink.textContent = '@' + profile.user.username.toLowerCase();
                        console.log(typeof profile.user.id);

                        const profileTitleContainer = document.createElement('div');
                        profileTitleContainer.classList.add('d-flex', 'titlecontainer');
                        profileTitleContainer.appendChild(profileTitle);
                        profileTitleContainer.appendChild(profileTitleMiddle);
                        profileTitleContainer.appendChild(profileLink);

                        const profileLastUpdated = document.createElement('small');
                        profileLastUpdated.classList.add('card-text', 'text-muted');
                        var dateString = profile.date;
                        var dateObject = new Date(dateString);
                        var day = dateObject.getDate();
                        var month = dateObject.toLocaleString('en-US', { month: 'long' });
                        var year = dateObject.getFullYear();
                        var hours = dateObject.getHours();
                        var minutes = dateObject.getMinutes();
                        profileLastUpdated.textContent = 'Last updated: ' + day + ' ' + month + ' ' + year + ' ' + hours + ':' + (minutes < 10 ? '0' : '') + minutes;

                        const profileBio = document.createElement('p');
                        profileBio.classList.add('card-text');
                        profileBio.textContent = profile.profile_bio;

                        profileCardBody.appendChild(profileTitleContainer);
                        profileCardBody.appendChild(profileLastUpdated);
                        profileCardBody.appendChild(profileBio);
                        profileInfoCol.appendChild(profileCardBody);
                        profileRow.appendChild(profileImageCol);
                        profileRow.appendChild(profileInfoCol);
                        profileElement.appendChild(profileRow);
                        profileListElement.appendChild(profileElement);
                        hoverEffect(profileElement);
                    });
                    nextPage++;

                    if (data.next) {
                        loadMoreButton.style.display = 'block';
                    } else {
                        loadMoreButton.style.display = 'none';
                    }
                });
        }

        fetchProfiles();
        loadMoreButton.addEventListener('click', fetchProfiles);
    }
}