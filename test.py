from SpoofedEmail import Email

# Menyiapkan email dengan alamat pengirim palsu
email = Email(
    sender="donotreply@register-sc.moonton.com",  # Pengirim palsu
    recipient="bahanstoree@gmail.com",  # Penerima
    subject="Mobile Legends: Bang Bang",  # Subjek
    message="This is a tes email, it appears to come from a different address."  # Isi email
)

# Mengirim email
email.send()
print("Email sent successfully!")
