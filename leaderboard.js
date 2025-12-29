// Fetch leaderboard data from API
async function loadLeaderboard() {
    try {
        const response = await fetch('/api/leaderboard');
        const users = await response.json();

        const tbody = document.getElementById("leaderboard-body");

        users.forEach((user, index) => {
            const row = document.createElement("tr");

            let rankClass = "rank";
            if (index === 0) rankClass += " gold";
            else if (index === 1) rankClass += " silver";
            else if (index === 2) rankClass += " bronze";

            row.innerHTML = `
                <td class="${rankClass}">#${index + 1}</td>
                <td>
                    <div class="user">
                        <div class="avatar">${user.username[0].toUpperCase()}</div>
                        <div class="username">${user.username}</div>
                    </div>
                </td>
                <td>${user.repos}</td>
                <td>${user.stars}</td>
                <td>${user.commits}</td>
                <td>${user.followers}</td>
                <td class="score">${user.score}</td>
                <td>${user.projects.join(', ')}</td>
            `;

            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading leaderboard:', error);
    }
}

// Load leaderboard when page loads
document.addEventListener('DOMContentLoaded', loadLeaderboard);

