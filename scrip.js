//chrome webrower-->inspect --> console
function scrapeImageURLs() {
    var urls = [];
    // Lấy tất cả các thẻ img trong trang
    var images = document.querySelectorAll('img');

    images.forEach(function(image) {
        var src = image.getAttribute('src');
        // Kiểm tra xem đường dẫn của hình ảnh có phải là URL hợp lệ không
        if (src && src.startsWith('http')) {
            urls.push(src);
        }
    });

    return urls;
}

function createDownload(urls) {
    var contents = urls.join('\n');
    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:attachment/text,' + encodeURI(contents);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'image_urls.txt';
    hiddenElement.click();
}

var imageUrls = scrapeImageURLs();
createDownload(imageUrls);
