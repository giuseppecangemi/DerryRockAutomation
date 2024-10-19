import qrcode

# URL
form_url = 'https://github.com/giuseppecangemi'

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(form_url)
qr.make(fit=True)

# saving
img = qr.make_image(fill='black', back_color='white')
img.save('/Users/giuseppecangemi/Downloads/derryrockpubfidelity.png')

print("QR code generato e salvato come 'qrcode_google_form.png'.")
