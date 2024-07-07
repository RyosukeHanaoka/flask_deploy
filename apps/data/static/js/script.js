document.addEventListener('DOMContentLoaded', function() {
    updateCheckboxPositions(); // 初期位置を設定

    // ウィンドウサイズが変更されたときに位置を再調整
    window.addEventListener('resize', updateCheckboxPositions);
});

function updateCheckboxPositions() {
    const imageContainer = document.getElementById('imageContainer');
    const containerWidth = imageContainer.offsetWidth;
    const containerHeight = imageContainer.offsetHeight;

    const checkboxes = document.querySelectorAll('#imageContainer .checkbox');
    checkboxes.forEach(function(checkbox) {
        const xPercentage = checkbox.dataset.x;
        const yPercentage = checkbox.dataset.y;
        const x = (parseFloat(xPercentage) / 100) * containerWidth;
        const y = (parseFloat(yPercentage) / 100) * containerHeight;
        checkbox.style.left = `${x}px`;
        checkbox.style.top = `${y}px`;
    });
}




