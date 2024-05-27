var originalTexts = {};

$(document).ready(function () {
    // Store original texts
    $('body :not(script)').contents().each(function () {
        if (this.nodeType === 3) {
            var original = $.trim($(this).text());
            if (original !== '') {
                var key = 'text_' + original;
                if (!originalTexts[key]) {
                    originalTexts[key] = original;
                    $(this).replaceWith('<span data-original="' + key + '">' + original + '</span>');
                }
            }
        } else if (this.nodeType === 1) {
            $.each(this.attributes, function () {
                var attrValue = $.trim(this.value);
                if (attrValue !== '') {
                    var key = 'attr_' + attrValue;
                    if (!originalTexts[key]) {
                        originalTexts[key] = attrValue;
                        $(this).attr('data-' + this.name + '-original', key);
                    }
                }
            });
        }
    });

    $('#language').change(function () {
        var lang = $(this).val();
        translatePage(lang);
    });
});

function translatePage(language) {
    $('[data-original]').each(function () {
        var originalKey = $(this).attr('data-original');
        var originalText = originalTexts[originalKey];
        $.ajax({
            url: 'https://api.mymemory.translated.net/get?q=' + originalText + '&langpair=en|' + language,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $(this).text(data.responseData.translatedText);
            }.bind(this),
            error: function (xhr, status, error) {
                console.error(xhr);
            }
        });
    });

    $('[data-src-original]').each(function () {
        var originalKey = $(this).attr('data-src-original');
        var originalText = originalTexts[originalKey];
        $.ajax({
            url: 'https://api.mymemory.translated.net/get?q=' + originalText + '&langpair=en|' + language,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $(this).attr('src', data.responseData.translatedText);
            }.bind(this),
            error: function (xhr, status, error) {
                console.error(xhr);
            }
        });
    });
}