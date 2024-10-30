import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(
        page_title="자동차 운전 게임",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # CSS for the game
    st.markdown("""
        <style>
            .stApp {
                background-color: #333;
            }
            iframe {
                border: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # JavaScript game code
    game_html = """
    <div style="width:100%; height:100vh;">
        <div id="gameContainer" style="width:100%; height:90vh; position:relative; overflow:hidden; background:#333;">
            <div id="road" style="width:100%; height:100%; position:absolute;"></div>
            <div id="car" style="width:60px; height:100px; position:absolute; bottom:20%; left:50%; transform:translateX(-50%);">
                <svg viewBox="0 0 60 100">
                    <rect x="10" y="10" width="40" height="80" rx="10" fill="#4A90E2"/>
                    <rect x="5" y="30" width="50" height="40" rx="5" fill="#5DA0E2"/>
                    <circle cx="15" cy="85" r="10" fill="#333"/>
                    <circle cx="45" cy="85" r="10" fill="#333"/>
                </svg>
            </div>
            <div id="score" style="position:absolute; top:20px; right:20px; color:white; font-size:24px;">점수: 0</div>
            <div id="gameOver" style="display:none; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); 
                                    background:rgba(0,0,0,0.8); color:white; padding:20px; text-align:center; border-radius:10px;">
                게임 오버!<br>
                <button onclick="restartGame()" style="margin-top:10px; padding:10px 20px; font-size:16px; cursor:pointer; 
                                                      background:#4A90E2; border:none; color:white; border-radius:5px;">
                    다시 시작
                </button>
            </div>
        </div>
        
        <script>
            const gameContainer = document.getElementById('gameContainer');
            const car = document.getElementById('car');
            const road = document.getElementById('road');
            const scoreElement = document.getElementById('score');
            const gameOverScreen = document.getElementById('gameOver');
            
            let score = 0;
            let isGameOver = false;
            let carPosition = 50;
            const carSpeed = 5;
            let obstacles = [];
            let bullets = [];
            
            // Road animation
            road.style.background = `repeating-linear-gradient(
                0deg,
                #333 0px,
                #333 50px,
                #555 50px,
                #555 100px
            )`;
            road.style.animation = 'roadMove 1s linear infinite';
            
            // Add animation keyframes
            const style = document.createElement('style');
            style.textContent = `
                @keyframes roadMove {
                    from { background-position: 0 0; }
                    to { background-position: 0 100px; }
                }
            `;
            document.head.appendChild(style);
            
            // Keyboard controls
            document.addEventListener('keydown', (e) => {
                if (isGameOver) return;
                
                if (e.key === 'ArrowLeft') {
                    carPosition = Math.max(10, carPosition - carSpeed);
                    car.style.left = carPosition + '%';
                }
                if (e.key === 'ArrowRight') {
                    carPosition = Math.min(90, carPosition + carSpeed);
                    car.style.left = carPosition + '%';
                }
                if (e.key === ' ') {
                    shoot();
                }
            });
            
            function shoot() {
                const bullet = document.createElement('div');
                bullet.className = 'bullet';
                bullet.style.position = 'absolute';
                bullet.style.width = '10px';
                bullet.style.height = '20px';
                bullet.style.backgroundColor = 'yellow';
                bullet.style.borderRadius = '5px';
                
                const carRect = car.getBoundingClientRect();
                bullet.style.left = (carRect.left + carRect.width/2 - 5) + 'px';
                bullet.style.top = carRect.top + 'px';
                
                gameContainer.appendChild(bullet);
                bullets.push(bullet);
            }
            
            function createObstacle() {
                if (isGameOver) return;
                
                const obstacle = document.createElement('div');
                obstacle.className = 'obstacle';
                obstacle.style.position = 'absolute';
                obstacle.style.width = '50px';
                obstacle.style.height = '80px';
                obstacle.style.backgroundColor = 'red';
                obstacle.style.top = '-80px';
                obstacle.style.left = Math.random() * (gameContainer.clientWidth - 50) + 'px';
                
                gameContainer.appendChild(obstacle);
                obstacles.push(obstacle);
            }
            
            function updateGame() {
                if (isGameOver) return;
                
                // Move bullets
                bullets.forEach((bullet, index) => {
                    const top = bullet.offsetTop;
                    if (top < 0) {
                        bullet.remove();
                        bullets.splice(index, 1);
                    } else {
                        bullet.style.top = (top - 10) + 'px';
                        checkBulletCollision(bullet);
                    }
                });
                
                // Move obstacles
                obstacles.forEach((obstacle, index) => {
                    const top = obstacle.offsetTop;
                    if (top > gameContainer.clientHeight) {
                        obstacle.remove();
                        obstacles.splice(index, 1);
                        score += 10;
                        scoreElement.textContent = '점수: ' + score;
                    } else {
                        obstacle.style.top = (top + 5) + 'px';
                        checkCollision(obstacle);
                    }
                });
            }
            
            function checkBulletCollision(bullet) {
                const bulletRect = bullet.getBoundingClientRect();
                obstacles.forEach((obstacle, index) => {
                    const obstacleRect = obstacle.getBoundingClientRect();
                    if (!(bulletRect.right < obstacleRect.left || 
                          bulletRect.left > obstacleRect.right || 
                          bulletRect.bottom < obstacleRect.top || 
                          bulletRect.top > obstacleRect.bottom)) {
                        obstacle.remove();
                        obstacles.splice(index, 1);
                        bullet.remove();
                        bullets.splice(bullets.indexOf(bullet), 1);
                        score += 20;
                        scoreElement.textContent = '점수: ' + score;
                    }
                });
            }
            
            function checkCollision(obstacle) {
                const carRect = car.getBoundingClientRect();
                const obstacleRect = obstacle.getBoundingClientRect();
                
                if (!(carRect.right < obstacleRect.left || 
                      carRect.left > obstacleRect.right || 
                      carRect.bottom < obstacleRect.top || 
                      carRect.top > obstacleRect.bottom)) {
                    gameOver();
                }
            }
            
            function gameOver() {
                isGameOver = true;
                gameOverScreen.style.display = 'block';
            }
            
            function restartGame() {
                isGameOver = false;
                score = 0;
                scoreElement.textContent = '점수: 0';
                gameOverScreen.style.display = 'none';
                carPosition = 50;
                car.style.left = '50%';
                
                obstacles.forEach(obstacle => obstacle.remove());
                obstacles = [];
                bullets.forEach(bullet => bullet.remove());
                bullets = [];
            }
            
            // Game loop
            setInterval(createObstacle, 2000);
            setInterval(updateGame, 20);
        </script>
    </div>
    """
    
    # Render the game
    components.html(game_html, height=800)

if __name__ == "__main__":
    main()