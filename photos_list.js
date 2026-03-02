// Lista de fotos - XV Anos Karla Lizbeth Bustamante
// Ejecuta generate_photo_list.py para regenerar este archivo

const photos = [];

window.addEventListener('DOMContentLoaded', function() {
    console.log(`Cargadas ${photos.length} fotos`);
    renderGallery();
    updateStats();
});
