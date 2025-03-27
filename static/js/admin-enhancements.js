/**
 * Admin paneli için JavaScript geliştirmeleri
 * CKEditor için özel yapılandırmalar ve görsel işleme iyileştirmeleri
 */

document.addEventListener('DOMContentLoaded', function() {
    // Yazar alanını mevcut kullanıcı olarak otomatik ayarla
    autoSelectCurrentUser();
    
    // İleri tarihli yayınlama özelliği
    initScheduledPublishing();
    
    // Admin panelinde CKEditor yüklendiğinde ek özelleştirmeler yapma
    if (typeof CKEDITOR !== 'undefined') {
        CKEDITOR.on('instanceReady', function(evt) {
            var editor = evt.editor;
            
            // Görsel ekleme dialogi açıldığında özel yapılandırmalar
            editor.on('dialogShow', function(dialogEvt) {
                var dialog = dialogEvt.data;
                
                // Görsel dialog'u içinse
                if (dialog.getName() === 'image' || dialog.getName() === 'image2') {
                    // Dialog başlığını Türkçe yapalım
                    dialog.setTitle('Görsel Ekle');
                    
                    // Otonom boyutlandırma seçeneği ekleyelim (dialog içeriğine erişip yeni seçenek ekleyeceğiz)
                    setTimeout(function() {
                        // Bazı dialog versiyonlarında farklı sekmeler ve alanlar olabiliyor, o yüzden try-catch kullanıyoruz
                        try {
                            // Önce dialog içeriğini bulalım
                            var contents = dialog.parts.contents;
                            if (!contents) return;
                            
                            // Seçenek alanını bulalım (farklı CKEditor versiyonlarında id'ler değişebilir)
                            var advancedTab = contents.querySelector('#tab-adv') || contents.querySelector('.ImageSize');
                            if (!advancedTab) return;
                            
                            // Yeni özel boyutlandırma seçeneği için bir div oluşturalım
                            var autoSizeContainer = document.createElement('div');
                            autoSizeContainer.className = 'auto-size-options';
                            autoSizeContainer.style.marginTop = '15px';
                            autoSizeContainer.style.padding = '10px';
                            autoSizeContainer.style.backgroundColor = '#f8f8f8';
                            autoSizeContainer.style.borderRadius = '4px';
                            
                            // Başlık ekleyelim
                            var autoSizeTitle = document.createElement('h3');
                            autoSizeTitle.innerText = 'Otomatik Boyutlandırma';
                            autoSizeTitle.style.fontSize = '14px';
                            autoSizeTitle.style.marginBottom = '10px';
                            autoSizeTitle.style.color = '#333';
                            autoSizeContainer.appendChild(autoSizeTitle);
                            
                            // Açıklama ekleyelim
                            var autoSizeDesc = document.createElement('p');
                            autoSizeDesc.innerText = 'Görselin kalitesini ve oranını bozmadan otomatik boyutlandırma için bir stil seçin:';
                            autoSizeDesc.style.fontSize = '12px';
                            autoSizeDesc.style.marginBottom = '8px';
                            autoSizeContainer.appendChild(autoSizeDesc);
                            
                            // Seçenek butonlarını ekleyelim
                            var autoSizeOptions = [
                                { id: 'auto', label: 'Otomatik', cssClass: 'img-auto', description: 'İçeriğe göre ayarlanır' },
                                { id: 'responsive', label: 'Duyarlı', cssClass: 'img-responsive', description: 'Tüm cihazlara uyum sağlar' },
                                { id: 'hq', label: 'Yüksek Kalite', cssClass: 'img-hq', description: 'Kaliteyi korur' },
                                { id: 'smart', label: 'Akıllı', cssClass: 'img-smart', description: 'Her cihaza uyarlanır' }
                            ];
                            
                            var optionsWrapper = document.createElement('div');
                            optionsWrapper.style.display = 'flex';
                            optionsWrapper.style.flexWrap = 'wrap';
                            optionsWrapper.style.gap = '8px';
                            
                            autoSizeOptions.forEach(function(option) {
                                var button = document.createElement('button');
                                button.type = 'button';
                                button.innerText = option.label;
                                button.title = option.description;
                                button.setAttribute('data-class', option.cssClass);
                                button.style.padding = '5px 10px';
                                button.style.border = '1px solid #ccc';
                                button.style.borderRadius = '3px';
                                button.style.backgroundColor = '#fff';
                                button.style.cursor = 'pointer';
                                button.style.fontSize = '12px';
                                
                                // Butona tıklandığında
                                button.addEventListener('click', function() {
                                    // Diğer tüm butonların seçilmişliğini kaldır
                                    optionsWrapper.querySelectorAll('button').forEach(function(btn) {
                                        btn.style.backgroundColor = '#fff';
                                        btn.style.color = '#333';
                                    });
                                    
                                    // Bu butonu seçili hale getir
                                    button.style.backgroundColor = '#0073aa';
                                    button.style.color = '#fff';
                                    
                                    // Görsele uygulanacak CSS sınıfını kaydet
                                    dialog.getContentElement('info', 'txtAlt') || dialog.getContentElement('advanced', 'advCSSClasses');
                                    
                                    // CSS sınıfı alanını bul ve değerini ayarla
                                    var classField = dialog.getContentElement('advanced', 'advCSSClasses') || 
                                                    dialog.getContentElement('info', 'txtGenClass');
                                    
                                    if (classField) {
                                        var currentClasses = classField.getValue() || '';
                                        
                                        // Önceki otomatik boyutlandırma sınıflarını kaldır
                                        currentClasses = currentClasses.replace(/img-auto|img-responsive|img-hq|img-smart/g, '').trim();
                                        
                                        // Yeni sınıfı ekle
                                        currentClasses = (currentClasses + ' ' + option.cssClass).trim();
                                        
                                        // Input alanını güncelle
                                        classField.setValue(currentClasses);
                                    }
                                });
                                
                                optionsWrapper.appendChild(button);
                            });
                            
                            autoSizeContainer.appendChild(optionsWrapper);
                            
                            // Container'ı Advanced tabına ekle
                            advancedTab.appendChild(autoSizeContainer);
                        } catch(e) {
                            console.error('Otomatik boyutlandırma seçenekleri eklenirken hata:', e);
                        }
                    }, 200);
                    
                    // Ek bilgilendirme metni ekleyelim
                    var infoDiv = document.createElement('div');
                    infoDiv.className = 'cke-image-info';
                    infoDiv.innerHTML = 'Görseli ekledikten sonra üzerine çift tıklayarak özelliklerini düzenleyebilirsiniz. "Otomatik Boyutlandırma" seçenekleri ile görselin boyutu ve kalitesi korunur.';
                    infoDiv.style.color = '#666';
                    infoDiv.style.padding = '5px';
                    infoDiv.style.marginTop = '10px';
                    infoDiv.style.borderTop = '1px solid #eee';
                    infoDiv.style.fontSize = '12px';
                    
                    // Dialog kapanmadan önce bilgilendirmeyi ekleyelim
                    setTimeout(function() {
                        // Dialog içeriğindeki uygun bir yere ekleyelim
                        var contentsElement = dialog.parts.contents;
                        if (contentsElement) {
                            contentsElement.appendChild(infoDiv);
                        }
                    }, 100);
                }
            });
            
            // Görsel eklendiğinde otomatik olarak duyarlı hale getir
            editor.on('insertElement', function(evt) {
                var element = evt.data;
                if (element && element.is('img') && !element.hasClass('img-auto') && 
                   !element.hasClass('img-responsive') && !element.hasClass('img-hq') && 
                   !element.hasClass('img-smart')) {
                    
                    // Varsayılan olarak duyarlı sınıfını ekle
                    element.addClass('img-responsive');
                    
                    // Eklenen görseli seç
                    editor.getSelection().selectElement(element);
                }
            });
            
            // Görsel seçildiğinde otomatik olarak düzenleme seçeneklerini göster
            editor.on('selectionChange', function(evt) {
                var selection = evt.editor.getSelection();
                if (selection) {
                    var element = selection.getStartElement();
                    if (element && element.is('img')) {
                        console.log('Görsel seçildi:', element);
                    }
                }
            });
        });
    }
    
    // Slug otomatik oluşturma geliştirmesi
    var titleInput = document.getElementById('id_title');
    var slugInput = document.getElementById('id_slug');
    
    if (titleInput && slugInput) {
        // Eğer slug alanı boşsa, başlık değiştiğinde otomatik oluştur
        titleInput.addEventListener('blur', function() {
            if (!slugInput.value.trim()) {
                // Basit bir slug oluşturucu (gelişmiş versiyonlar için slugify kullanılabilir)
                var slug = titleInput.value.trim()
                    .toLowerCase()
                    .replace(/[^a-z0-9\s-]/g, '') // Özel karakterleri kaldır
                    .replace(/\s+/g, '-')         // Boşlukları tire ile değiştir
                    .replace(/-+/g, '-')          // Ardışık tireleri tekleştir
                    .substring(0, 50);            // 50 karakterle sınırla
                
                slugInput.value = slug;
            }
        });
    }
    
    // Featured Image önizleme ve optimizasyon geliştirmesi
    var featuredImageInput = document.getElementById('id_featured_image');
    if (featuredImageInput) {
        // Otonom boyutlandırma seçenekleri konteynerini oluştur
        var optimizeOptions = document.createElement('div');
        optimizeOptions.className = 'image-optimize-options';
        optimizeOptions.style.marginTop = '10px';
        optimizeOptions.style.padding = '10px';
        optimizeOptions.style.backgroundColor = '#f9f9f9';
        optimizeOptions.style.border = '1px solid #e0e0e0';
        optimizeOptions.style.borderRadius = '4px';
        
        // Başlık ekle
        var optionsTitle = document.createElement('h4');
        optionsTitle.textContent = 'Görsel Optimizasyonu';
        optionsTitle.style.margin = '0 0 10px 0';
        optionsTitle.style.fontSize = '14px';
        optimizeOptions.appendChild(optionsTitle);
        
        // Açıklama ekle
        var optionsDesc = document.createElement('p');
        optionsDesc.textContent = 'Yüklenen görselin otomatik boyutlandırma seçenekleri:';
        optionsDesc.style.margin = '0 0 10px 0';
        optionsDesc.style.fontSize = '12px';
        optimizeDesc.style.color = '#666';
        optimizeOptions.appendChild(optionsDesc);
        
        // Seçenekler
        var optimizeSettings = [
            { id: 'preserve_ratio', label: 'En-boy oranını koru', checked: true },
            { id: 'auto_resize', label: 'Otomatik boyutlandır', checked: true },
            { id: 'high_quality', label: 'Yüksek kalite', checked: true }
        ];
        
        // Seçenekleri ekle
        optimizeSettings.forEach(function(setting) {
            var optionContainer = document.createElement('div');
            optionContainer.style.marginBottom = '5px';
            
            var checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = setting.id;
            checkbox.checked = setting.checked;
            checkbox.style.marginRight = '5px';
            
            var label = document.createElement('label');
            label.htmlFor = setting.id;
            label.textContent = setting.label;
            label.style.fontSize = '13px';
            label.style.fontWeight = 'normal';
            
            optionContainer.appendChild(checkbox);
            optionContainer.appendChild(label);
            optimizeOptions.appendChild(optionContainer);
        });
        
        // Önizleme konteynerini oluştur
        var previewContainer = document.createElement('div');
        previewContainer.id = 'image-preview-container';
        previewContainer.style.marginTop = '10px';
        previewContainer.style.textAlign = 'center';
        previewContainer.style.display = 'none';
        
        // Önizleme olarak kullanılacak <img> elementi
        var previewImg = document.createElement('img');
        previewImg.id = 'image-preview';
        previewImg.style.maxHeight = '250px';
        previewImg.style.maxWidth = '100%';
        previewImg.style.borderRadius = '4px';
        previewImg.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
        previewContainer.appendChild(previewImg);
        
        // Değerleri göstermek için bilgi konteynerini ekle
        var imageInfoContainer = document.createElement('div');
        imageInfoContainer.className = 'image-info';
        imageInfoContainer.style.marginTop = '8px';
        imageInfoContainer.style.fontSize = '12px';
        imageInfoContainer.style.color = '#666';
        previewContainer.appendChild(imageInfoContainer);
        
        // Optimizasyon seçeneklerini input alanından sonra ekleyelim
        featuredImageInput.parentNode.appendChild(optimizeOptions);
        featuredImageInput.parentNode.appendChild(previewContainer);
        
        // Görsel değiştiğinde
        featuredImageInput.addEventListener('change', function(e) {
            var file = this.files[0];
            if (file && file.type.match('image.*')) {
                var reader = new FileReader();
                
                reader.onload = function(e) {
                    // Görsel bilgilerini hesapla
                    var img = new Image();
                    img.onload = function() {
                        var width = this.width;
                        var height = this.height;
                        var fileSize = (file.size / 1024).toFixed(2) + ' KB';
                        
                        // Bilgi alanını güncelle
                        imageInfoContainer.innerHTML = 
                            'Orijinal Boyut: ' + width + 'x' + height + ' px<br>' +
                            'Dosya Boyutu: ' + fileSize + '<br>' +
                            'Format: ' + file.type.split('/')[1].toUpperCase();
                        
                        // Optimizasyon seçeneklerini güncelle
                        var preserveRatio = document.getElementById('preserve_ratio');
                        var autoResize = document.getElementById('auto_resize');
                        var highQuality = document.getElementById('high_quality');
                        
                        // Orijinal görüntüyü göster
                        previewImg.src = e.target.result;
                        previewImg.style.maxHeight = '250px';
                        
                        // Önizleme için ayarları uygula
                        if (preserveRatio && preserveRatio.checked) {
                            previewImg.style.objectFit = 'contain';
                        }
                        
                        if (autoResize && autoResize.checked) {
                            previewImg.classList.add('img-responsive');
                        } else {
                            previewImg.classList.remove('img-responsive');
                        }
                        
                        if (highQuality && highQuality.checked) {
                            previewImg.classList.add('img-hq');
                        } else {
                            previewImg.classList.remove('img-hq');
                        }
                        
                        // Önizlemeyi göster
                        previewContainer.style.display = 'block';
                    };
                    img.src = e.target.result;
                    
                    // Eğer başlık alanı varsa göster
                    var caption = document.getElementById('id_featured_image_caption');
                    if (caption) {
                        caption.style.display = 'block';
                    }
                };
                
                reader.readAsDataURL(file);
            }
        });
    }
});

/**
 * İleri tarihli yayınlama özelliğini başlatır
 */
function initScheduledPublishing() {
    // Status ve published_at alanlarını al
    var statusField = document.getElementById('id_status');
    var publishedAtField = document.getElementById('id_published_at');
    
    if (statusField && publishedAtField) {
        // Status alanının kapsayıcısını al (fieldset)
        var publishingFieldset = publishedAtField.closest('fieldset');
        
        if (publishingFieldset) {
            // İleri tarihli yayınlama için açıklama ekle
            var scheduleInfo = document.createElement('div');
            scheduleInfo.className = 'scheduled-publishing-info';
            scheduleInfo.style.backgroundColor = '#e5f7ff';
            scheduleInfo.style.padding = '10px 15px';
            scheduleInfo.style.borderRadius = '5px';
            scheduleInfo.style.marginTop = '10px';
            scheduleInfo.style.marginBottom = '15px';
            scheduleInfo.style.border = '1px solid #b5e3ff';
            scheduleInfo.innerHTML = `
                <h3 style="margin-top:0; margin-bottom:8px; font-size:14px; color:#0073aa;">
                    <i class="fas fa-calendar-alt"></i> İleri Tarihli Yayınlama
                </h3>
                <p style="margin-bottom:5px; font-size:13px; color:#333;">
                    Eğer yazınızı ileri bir tarihte yayınlamak istiyorsanız:
                </p>
                <ol style="margin-top:0; padding-left:25px; font-size:13px; color:#333;">
                    <li>Durumu <strong>Yayınlandı</strong> olarak seçin</li>
                    <li><strong>Yayın Tarihi</strong> alanına istediğiniz tarih ve saati girin</li>
                    <li>Sistem bu tarih geldiğinde yazıyı otomatik olarak yayınlayacaktır</li>
                </ol>
                <p style="margin-bottom:0; font-size:13px; color:#666; font-style:italic;">
                    İleri tarihli yazılar sadece yazara ve yöneticilere görünür.
                </p>
            `;
            
            // Açıklamayı status alanından sonra ekle
            statusField.closest('.field-status').after(scheduleInfo);
            
            // Tarih-saat seçiciyi geliştir
            enhanceDateTimePicker(publishedAtField);
            
            // İleri tarihli yayın için hızlı zamanlar ekle
            addQuickScheduleOptions(publishedAtField);
            
            // Status değiştiğinde published_at alanını güncelle
            statusField.addEventListener('change', function() {
                handleStatusChange(statusField, publishedAtField);
            });
            
            // Sayfa yüklendiğinde bir kez çalıştır
            handleStatusChange(statusField, publishedAtField);
        }
    }
}

/**
 * Yayın durumu değiştiğinde published_at alanını günceller
 */
function handleStatusChange(statusField, publishedAtField) {
    if (statusField.value === 'published') {
        // Yayınlandı seçildiğinde published_at alanını görünür yap
        publishedAtField.closest('.field-published_at').style.display = 'block';
        
        // Eğer tarih boşsa şimdiki zamanı ata
        if (!publishedAtField.value.trim()) {
            // Güncel tarih ve zamanı ata (yerel saat dilimine göre)
            var now = new Date();
            var year = now.getFullYear();
            var month = String(now.getMonth() + 1).padStart(2, '0');
            var day = String(now.getDate()).padStart(2, '0');
            var hours = String(now.getHours()).padStart(2, '0');
            var minutes = String(now.getMinutes()).padStart(2, '0');
            
            publishedAtField.value = `${year}-${month}-${day} ${hours}:${minutes}:00`;
        }
    } else {
        // Taslak seçildiğinde published_at alanını gizle ve boşalt
        publishedAtField.closest('.field-published_at').style.display = 'none';
        publishedAtField.value = '';
    }
}

/**
 * Tarih-saat seçiciyi geliştirir
 */
function enhanceDateTimePicker(publishedAtField) {
    // Tarih alanını daha belirgin hale getir
    publishedAtField.style.fontSize = '14px';
    publishedAtField.style.padding = '8px 10px';
    publishedAtField.style.borderColor = '#3498db';
    publishedAtField.style.backgroundColor = '#f8f9fa';
    publishedAtField.style.width = '250px';
    
    // Yayın tarihi alanına odaklanıldığında kullanım önerisi ekle
    var dateHelpText = document.createElement('p');
    dateHelpText.className = 'datetime-help';
    dateHelpText.innerHTML = 'Format: <code>YYYY-MM-DD HH:MM:SS</code>';
    dateHelpText.style.fontSize = '12px';
    dateHelpText.style.marginTop = '5px';
    dateHelpText.style.color = '#666';
    
    publishedAtField.parentNode.appendChild(dateHelpText);
}

/**
 * İleri tarihli yayın için hızlı seçenekler ekler
 */
function addQuickScheduleOptions(publishedAtField) {
    var quickOptions = document.createElement('div');
    quickOptions.className = 'quick-schedule-options';
    quickOptions.style.marginTop = '10px';
    
    // Hızlı seçenekler başlığı
    var optionsTitle = document.createElement('p');
    optionsTitle.textContent = 'Hızlı Seçenekler:';
    optionsTitle.style.fontSize = '13px';
    optionsTitle.style.fontWeight = 'bold';
    optionsTitle.style.marginBottom = '5px';
    quickOptions.appendChild(optionsTitle);
    
    // Hızlı seçenek butonları
    var options = [
        { label: 'Şimdi', value: 0 },
        { label: '1 Saat Sonra', value: 1 },
        { label: '3 Saat Sonra', value: 3 },
        { label: 'Yarın', value: 24 },
        { label: '2 Gün Sonra', value: 48 },
        { label: '1 Hafta Sonra', value: 168 }
    ];
    
    // Butonları içeren konteyner
    var buttonContainer = document.createElement('div');
    buttonContainer.style.display = 'flex';
    buttonContainer.style.flexWrap = 'wrap';
    buttonContainer.style.gap = '8px';
    
    options.forEach(function(option) {
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'quick-schedule-btn';
        button.textContent = option.label;
        button.style.padding = '6px 10px';
        button.style.border = '1px solid #ccc';
        button.style.borderRadius = '4px';
        button.style.backgroundColor = '#fff';
        button.style.cursor = 'pointer';
        button.style.fontSize = '12px';
        
        // Hover efekti
        button.onmouseover = function() {
            this.style.backgroundColor = '#f0f0f0';
        };
        button.onmouseout = function() {
            this.style.backgroundColor = '#fff';
        };
        
        // Tıklama olayı
        button.addEventListener('click', function() {
            var date = new Date();
            
            // Belirtilen saat kadar ekle
            date.setHours(date.getHours() + option.value);
            
            var year = date.getFullYear();
            var month = String(date.getMonth() + 1).padStart(2, '0');
            var day = String(date.getDate()).padStart(2, '0');
            var hours = String(date.getHours()).padStart(2, '0');
            var minutes = String(date.getMinutes()).padStart(2, '0');
            
            publishedAtField.value = `${year}-${month}-${day} ${hours}:${minutes}:00`;
        });
        
        buttonContainer.appendChild(button);
    });
    
    quickOptions.appendChild(buttonContainer);
    publishedAtField.parentNode.appendChild(quickOptions);
}

/**
 * Giriş yapan kullanıcıyı otomatik olarak blog yazarı olarak seçer
 */
function autoSelectCurrentUser() {
    // Yazar seçme alanını bul
    var authorSelect = document.getElementById('id_author');
    
    if (authorSelect) {
        // URL'den yeni ekleme sayfasında olup olmadığımızı kontrol et
        // Yeni ekleme sayfasında URL genellikle "/add/" içerir
        var isAddPage = window.location.href.indexOf('/add/') > -1;
        
        // Eğer bir ekleme sayfasındaysak ve form boşsa
        if (isAddPage) {
            // Doğrudan JavaScript ile kullanıcı bilgisini alamayız, bu yüzden
            // Sayfada halihazırda seçili kullanıcı kimse onu kullanacağız.
            // Django admin paneli genellikle oturum açan kullanıcının bilgilerini
            // sayfanın üst kısmında gösterir.
            
            // Üst köşedeki kullanıcı adını bul
            var userText = document.querySelector('#user-tools strong');
            if (userText) {
                var currentUsername = userText.textContent.trim();
                
                // Eğer kullanıcı adını bulabildiyse, select listesinde ara
                if (currentUsername) {
                    // Select listesindeki tüm opsiyonları kontrol et
                    for (var i = 0; i < authorSelect.options.length; i++) {
                        var optionText = authorSelect.options[i].text;
                        
                        // Eğer opsiyon metni kullanıcı adını içeriyorsa seç
                        if (optionText.indexOf(currentUsername) > -1) {
                            authorSelect.selectedIndex = i;
                            
                            // Seçimi vurgula ve görünür hale getir
                            authorSelect.style.backgroundColor = '#e8f7ff';
                            authorSelect.style.borderColor = '#2271b1';
                            
                            // Select alanının yanına bilgilendirme metni ekle
                            var infoText = document.createElement('p');
                            infoText.className = 'author-auto-selected';
                            infoText.innerHTML = '<i class="fas fa-info-circle"></i> Siz yazar olarak otomatik seçildiniz.';
                            infoText.style.color = '#2271b1';
                            infoText.style.fontSize = '12px';
                            infoText.style.marginTop = '5px';
                            infoText.style.fontStyle = 'italic';
                            
                            // Select alanından sonraya ekle
                            if (authorSelect.parentNode) {
                                authorSelect.parentNode.appendChild(infoText);
                            }
                            
                            break;
                        }
                    }
                }
            }
        }
    }
} 