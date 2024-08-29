import sys
import dns.resolver
import concurrent.futures

def print_usage():
    print("Kullanım: python findthesub.py <domain> <wordlist_path> [output_file]")
    print("Örnek: python findthesub.py example.com wordlist.txt output.txt")

def check_subdomain(domain, subdomain, results):
    try:

        full_domain = f"{subdomain}.{domain}"

        answers = dns.resolver.resolve(full_domain, 'A')
        for answer in answers:
            result = f"Bulundu: {full_domain} -> {answer}"
            print(result)
            results.append(result)
    except dns.resolver.NoAnswer:
        pass
    except dns.resolver.NXDOMAIN:
        pass
    except Exception as e:
        print(f"Hata: {subdomain}.{domain} - {e}")

def main():

    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print_usage()
        sys.exit(1)
    domain = sys.argv[1]
    wordlist_path = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) == 4 else None
    try:
        with open(wordlist_path, "r") as file:
            subdomains = file.read().splitlines()
    except FileNotFoundError:
        print(f"Hata: {wordlist_path} dosyası bulunamadı.")
        sys.exit(1)

    results = []

  
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda sub: check_subdomain(domain, sub, results), subdomains)

    
    if output_file:
        try:
            with open(output_file, "w") as file:
                for line in results:
                    file.write(line + "\n")
            print(f"Sonuçlar {output_file} dosyasına kaydedildi.")
        except Exception as e:
            print(f"Hata: {output_file} dosyasına yazılamadı - {e}")

if __name__ == "__main__":
    main()
