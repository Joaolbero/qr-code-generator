import argparse
from pathlib import Path
import segno
from segno import helpers

def build_parser():
    p = argparse.ArgumentParser(
        description="QR Code Generator (text, Wi-Fi, vCard) — by João Vitor"
    )
    p.add_argument("--mode", choices=["text", "wifi", "vcard"], default="text",
                   help="Tipo de QR")
    # text
    p.add_argument("--data", help="Texto/URL (modo text)")
    # wifi
    p.add_argument("--ssid", help="SSID (modo wifi)")
    p.add_argument("--password", help="Senha (modo wifi)")
    p.add_argument("--security", choices=["WPA", "WEP", "nopass"], default="WPA",
                   help="Segurança Wi-Fi")
    p.add_argument("--hidden", action="store_true", help="SSID oculto (wifi)")
    # vcard
    p.add_argument("--name", help="Nome completo (vcard)")
    p.add_argument("--phone", help="Telefone (vcard)")
    p.add_argument("--email", help="E-mail (vcard)")
    p.add_argument("--org", help="Empresa (vcard)")
    # output
    p.add_argument("--outfile", required=True, help="Arquivo de saída (.png/.svg/.pdf/.eps)")
    p.add_argument("--scale", type=int, default=8, help="Escala para raster (PNG)")
    p.add_argument("--border", type=int, default=4, help="Borda (módulos)")
    p.add_argument("--error", choices=["L", "M", "Q", "H"], default="M",
                   help="Correção de erro (QR EC level)")
    return p

def _save_qr(qr, outpath: Path, scale: int, border: int):
    outpath.parent.mkdir(parents=True, exist_ok=True)
    suff = outpath.suffix.lower()
    if suff == ".png":
        qr.save(outpath, kind="png", scale=scale, border=border)
    elif suff in (".svg", ".pdf", ".eps"):
        qr.save(outpath, border=border)
    else:
        raise SystemExit("Use extensões .png, .svg, .pdf ou .eps")
    print(f"OK! Gerado: {outpath.resolve()}")

def make_qr(args):
    # --- TEXT / URL ---
    if args.mode == "text":
        if not args.data:
            raise SystemExit("Erro: --data é obrigatório no modo text")
        qr = segno.make(args.data, error=args.error)
        _save_qr(qr, Path(args.outfile), args.scale, args.border)
        return

    # --- WIFI ---
    if args.mode == "wifi":
        if not args.ssid:
            raise SystemExit("Erro: --ssid é obrigatório no modo wifi")
       
        security = None if args.security == "nopass" else args.security
        password = None if args.security == "nopass" else (args.password or "")

       
        data = None
        if hasattr(helpers, "make_wifi_data"):
            data = helpers.make_wifi_data(
                ssid=args.ssid,
                password=password,
                security=security,
                hidden=args.hidden
            )
        else:
            if security is None:
                data = f"WIFI:T:nopass;S:{args.ssid};{'H:true;' if args.hidden else ''};"
            else:
                data = f"WIFI:T:{security};S:{args.ssid};P:{password};{'H:true;' if args.hidden else ''};"

        qr = segno.make(data, error=args.error)
        _save_qr(qr, Path(args.outfile), args.scale, args.border)
        return

    # --- VCARD ---
    if args.mode == "vcard":
        if not args.name:
            raise SystemExit("Erro: --name é obrigatório no modo vcard")

        data = None
        if hasattr(helpers, "make_vcard_data"):
            data = helpers.make_vcard_data(
                name=args.name,
                displayname=args.name,
                phone=args.phone,
                email=args.email,
                org=args.org
            )
        else:
            # Fallback: vCard 3.0 simples (campos opcionais só se existirem)
            lines = [
                "BEGIN:VCARD",
                "VERSION:3.0",
                f"FN:{args.name}",
            ]
            if args.org:
                lines.append(f"ORG:{args.org}")
            if args.phone:
                lines.append(f"TEL:{args.phone}")
            if args.email:
                lines.append(f"EMAIL:{args.email}")
            lines.append("END:VCARD")
            data = "\n".join(lines)

        qr = segno.make(data, error=args.error)
        _save_qr(qr, Path(args.outfile), args.scale, args.border)
        return

def main():
    parser = build_parser()
    args = parser.parse_args()
    make_qr(args)

if __name__ == "__main__":
    main()