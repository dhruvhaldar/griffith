function drawCrack(width, crackLength) {
    const canvas = document.getElementById('crack-viewer');
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    // Clear canvas
    ctx.clearRect(0, 0, w, h);

    // Scale
    const margin = 40;
    const plateWidthPx = w - 2 * margin;
    const scale = plateWidthPx / width;

    // Plate dimensions
    // Assume height is proportional or fixed ratio for visualization
    const plateHeight = width * 1.5; // Example aspect ratio
    const plateHeightPx = plateHeight * scale;

    // Limit height to fit canvas
    const maxPlateHeightPx = h - 2 * margin;
    let finalScale = scale;
    if (plateHeightPx > maxPlateHeightPx) {
        finalScale = maxPlateHeightPx / plateHeight;
    }

    const pxWidth = width * finalScale;
    const pxHeight = plateHeight * finalScale;

    const startX = (w - pxWidth) / 2;
    const startY = (h - pxHeight) / 2;

    // Draw Plate
    ctx.fillStyle = '#e0e0e0';
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.fillRect(startX, startY, pxWidth, pxHeight);
    ctx.strokeRect(startX, startY, pxWidth, pxHeight);

    // Draw Crack (Center Crack)
    const crackLenPx = crackLength * finalScale;
    const crackY = startY + pxHeight / 2;
    const crackStartX = startX + (pxWidth - crackLenPx) / 2;
    const crackEndX = crackStartX + crackLenPx;

    ctx.beginPath();
    ctx.moveTo(crackStartX, crackY);
    ctx.lineTo(crackEndX, crackY);
    ctx.strokeStyle = 'red';
    ctx.lineWidth = 4;
    ctx.stroke();

    // Add text
    ctx.fillStyle = 'black';
    ctx.font = '14px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`Width: ${width} m`, w / 2, startY - 10);
    ctx.fillText(`Crack: ${crackLength} m`, w / 2, crackY - 10);
    ctx.fillText(`Plate`, w / 2, startY + pxHeight + 20);
}

// Initial draw
document.addEventListener('DOMContentLoaded', () => {
    drawCrack(0.1, 0.02);
});
