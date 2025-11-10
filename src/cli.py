import argparse
from pathlib import Path
import segno

def build_parser():
    p = argparse.ArgumentParser(
        description="QR Code Generator (text, Wi-Fi, vCard) — by João Vitor"
    )
    p.add_argument("--mode", choices=["text", "wifi", "vcard"], default="text",
                   help="Tipo de QR")
    p.add_argument("--data", help="Texto/URL (modo text)")
    p.add_argument("--ssid", help="SSID (modo wifi)")
    p.add_argument("--password", help="Senha (modo wifi)")
    p.add_argument("--security", choices=["WPA", "WEP", "nopass"], default="WPA",
                   help="Segurança Wi-Fi")
    p.add_argument("--hidden", action="store_true", help="SSID oculto (wifi)")
    p.add_argument("--name", help="Nome completo (vcard)")
    p.add_argument("--phone", help="Telefone (vcard)")
    p.add_argument("--email", help="E-mail (vcard)")
    p.add_argument("--org", help="Empresa (vcard)")
    p.add_argument("--outfile", required=True, help="Arquivo de saída (.png/.svg/.pdf/.eps)")
    p.add_argument("--scale", type=int, default=8, help="Escala para raster (PNG)")
    p.add_argument("--border", type=int, default=4, help="Borda (módulos)")
    p.add_argument("--error", choices=["L", "M", "Q", "H"], default="M",
                   help="Correção de erro")
    return p

def make_qr(args):
    if args.mode == "text":
        if not args.data:
            raise SystemExit("Erro: --data é obrigatório no modo text")
        qr = segno.make(args.data, error=args.error)

    elif args.mode == "wifi":
        if not args.ssid:
            raise SystemExit("Erro: --ssid é obrigatório no modo wifi")
        qr = segno.helpers.make_wifi(
            ssid=args.ssid,
            password=None if args.security == "nopass" else (args.password or ""),
            security=None if args.security == "nopass" else args.security,
            hidden=args.hidden,
            error=args.error
        )

    else:  # vcard
        if not args.name:
            raise SystemExit("Erro: --name é obrigatório no modo vcard")
        qr = segno.helpers.make_vcard(
            name=args.name,
            displayname=args.name,
            phone=args.phone,
            email=args.email,
            org=args.org,
            error=args.error
        )

    out = Path(args.outfile)
    out.parent.mkdir(parents=True, exist_ok=True)

    suff = out.suffix.lower()
    if suff == ".png":
        qr.save(out, scale=args.scale, border=args.border)
    elif suff in (".svg", ".pdf", ".eps"):
        qr.save(out, border=args.border)
    else:
        raise SystemExit("Use extensões .png, .svg, .pdf ou .eps")

    print(f"OK! Gerado: {out.resolve()}")

def main():
    parser = build_parser()
    args = parser.parse_args()
    make_qr(args)

if __name__ == "__main__":
    main()