from cryptography.fernet import Fernet

Key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcBuKEY90jAYaAaSsxFQCtdFs1malP-8gWIE9q2s6O73-gVlLdJaorTgddZiTKElwEFqWBqJPMV0uDSZgUW76Xcoa48jsMumwtCoxW76tLisp5-0rxAVxzxEcqfGF8iPgbzbzFPONeD_SG-tiaYVO90aCY7CeuS0GByNKDn2yFriHlnFWhLDcSm-LXa22aREgs6U4j'

def main():
    f = Fernet(Key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
