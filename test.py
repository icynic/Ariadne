test_cases = [
    # Web protocols
    "https://example.com/path",
    "http://sub.example.com:8080",
    
    # Local protocols
    "localhost:3000",
    "file:///C:/path/file.pdf",
    "file://laptop/shared/file.txt",
    "file://localhost/path/file.txt",
    
    # Network protocols
    "ftp://files.example.com",
    "sftp://user@server.com:22",
    "ssh://user:pass@192.168.1.1",
    "smb://fileserver/share",
    "ldap://ldap.example.com:389",
    
    # Special cases
    "file:///",
    "//server/share",
]

def parseURL(url:str):
    remainder=url
    if "//" in url:
        remainder = url.split('//', 1)[1]
        if remainder.startswith('/'):
            remainder=remainder[1:]
            return remainder
    remainder = remainder.split('/', 1)[0]
    return remainder

for i in test_cases:
    print(parseURL(i))