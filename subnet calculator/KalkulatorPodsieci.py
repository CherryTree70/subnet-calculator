import sys
import socket
import re
import json


def Check0_255(a):
    if a > -1 and a < 256:
        return 1
    else:
        return 0
def RegularExpression(adres):
    pattern = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$', str(adres))
    if pattern:
        return 1
    else:
        print("Nieprawidlowy format IP, odpowiedni to: XXX.XXX.XXX.XXX/XX")
        return 0
def ValidateIP(adres):
    if RegularExpression(adres):
        g = str(adres).split("/")
        subnetmask = g[1]
        ip = g[0].split(".")
        if Check0_255(int(ip[0])) and Check0_255(int(ip[1])) and Check0_255(int(ip[2])) and Check0_255(int(ip[3])):
            if 0 <= int(subnetmask) <= 32:
                return 1
            else:
                print("Maska nie miesci sie miedzi 0 - 32")
                return 0
        else:
            print("Jedna z wartosci poza 0-255")
            return 0
    else:
        return 0
def CidrToBinMask(cidr):
    pom = int(cidr)
    tab = []
    licz = 1
    for j in range(32):
        if pom > 0:
            tab.append("1")
            pom = pom - 1
        else:
            tab.append("0")
        if licz % 8 == 0 and licz != 0 and licz != 32:
            tab.append(".")
        licz = licz + 1
    Mask = ''.join(str(e) for e in tab)
    return Mask
def WebClass(FirstIPPart):
    FirstIPPart = int(FirstIPPart)
    if FirstIPPart <= 127:
        return "A"
    else:
        if FirstIPPart <= 191:
            return "B"
        else:
            if FirstIPPart <= 223:
                return "C"
            else:
                if FirstIPPart <= 239:
                    return "D"
                else:
                    return "E"
def DecToBin(ZmiennaDec):
    tab = []

    test = str(ZmiennaDec).split(".")
    for i in range (4):
        z = bin(int(test[i]))

        x = z.split("b")
        licznik = len(x[1])
        for j in range (8-licznik):
            tab.append("0")
        tab.append(str(x[1]))

        if i !=3:
            tab.append(".")
    ZmiennaBin = ''.join(tab)

    return ZmiennaBin
def BinToDec(ZmiennaBin):
    SpiltedBin = str(ZmiennaBin).split(".")
    tab = []
    for i in range (4):
        ZmiennaDec = int(SpiltedBin[i],2)
        tab.append(str(ZmiennaDec))
        if i != 3:
            tab.append(".")

    ZmiennaRet = ''.join(tab)
    return (ZmiennaRet)
def Address(Ip,Mask):
    IpSplited = Ip.split(".")
    MaskSplited = Mask.split(".")
    IPString = ''.join(IpSplited)
    MaskString = ''.join(MaskSplited)
    tab = []

    licznik = 1
    for i in range (0,32):
        pom = int(IPString[i]) * int(MaskString[i])
        tab.append(str(pom))
        if licznik%8 ==0 and i!=0 and i!=31:
            tab.append(".")
        licznik = licznik + 1


    Adres = ''.join(tab)
    return Adres
def Broadcast(AdresSieci, BinMask):
    pom = BinMask.split(".")
    MaskString = "".join(pom)
    tab = []
    licznik = 1
    for i in range (32):
        if MaskString[i] == "1":
            tab.append("0")
        else:
            tab.append("1")
        if licznik % 8 == 0 and i != 31:
            tab.append(".")
        licznik = licznik + 1

    MaskaNot = "".join(tab)
    MaskaNotDec = BinToDec(MaskaNot)
    splitMaska = MaskaNotDec.split(".")
    splitAdres = AdresSieci.split(".")
    tab2 = []
    for j in range (4):
        pom2 = int(splitMaska[j]) + int(splitAdres[j])
        tab2.append(str(pom2))
        if j != 3:
            tab2.append(".")

    BroadcastAdres = "".join(tab2)
    return (BroadcastAdres)
def NumberOfHosts(cidr):
    z = pow(2,32-int(cidr))
    return z-2
def FirstHost(AdresSieci):
    FirstHostAdres = []
    AdresSplit = AdresSieci.split(".")
    AdresSplit[3] = str(int(AdresSplit[3]) + 1)
    for i in range (4):
        FirstHostAdres.append(AdresSplit[i])
        if i!=3:
            FirstHostAdres.append(".")
    AdresPierwszegoKoncowy = "".join(FirstHostAdres)
    return AdresPierwszegoKoncowy
def LastHost(Broadcast):
    LastHostAdres = []
    AdresSplit = Broadcast.split(".")
    AdresSplit[3] = str(int(AdresSplit[3]) - 1)
    for i in range(4):
        LastHostAdres.append(AdresSplit[i])
        if i != 3:
            LastHostAdres.append(".")
    AdresOstatniegoKoncowy = "".join(LastHostAdres)
    return AdresOstatniegoKoncowy

if len(sys.argv) == 1:
    adres = socket.gethostbyname(socket.gethostname())
else:
    adres = sys.argv[1]

if ValidateIP(adres):
    print("Adres jest calkowicie prawidlowy")
    IP, cidr = str(adres).split("/")
    PartsIP = str(IP).split(".")
    AdresSieciBin = Address(DecToBin(IP), CidrToBinMask(cidr))
    AdresSieciDec = BinToDec(AdresSieciBin)
    KlasaSieci = WebClass(PartsIP[0])
    MaskaSieciDec = BinToDec(CidrToBinMask(cidr))
    MaskaSieciBin = CidrToBinMask(cidr)
    BroadcastDec = Broadcast (AdresSieciDec,CidrToBinMask(cidr))
    BroadcastBin = DecToBin(BroadcastDec)
    PierwszyHostDec = FirstHost(AdresSieciDec)
    PierwszyHostBin = DecToBin(PierwszyHostDec)
    OstatniHostDec = LastHost(BroadcastDec)
    OstatniHostBin = DecToBin(OstatniHostDec)
    MaxLiczbaHostowDec = NumberOfHosts(cidr)
    splitHost = str(bin(MaxLiczbaHostowDec)).split("b")
    MaxLiczbaHostowBin = splitHost[1]
    print ("Adres sieci bin: %s dec: %s" % (AdresSieciBin,AdresSieciDec))
    print ("Klasa sieci: %s"% (KlasaSieci))
    print ("Maska sieci: bin: %s dec: %s"% (MaskaSieciBin,MaskaSieciDec))
    print ("Adres broadcast: bin: %s dec: %s"% (BroadcastBin,BroadcastDec))
    print ("Pierwszy adres: bin: %s dec: %s" % (PierwszyHostBin, PierwszyHostDec))
    print ("Ostatni adres: bin: %s dec: %s" % (OstatniHostBin, OstatniHostDec))
    print ("Maksymalna ilosc hostow: bin: %s dec: %s" %(MaxLiczbaHostowBin, MaxLiczbaHostowDec))
    TabToJson = []
    TabToJson.append({'AdresSieciBin':AdresSieciBin})
    TabToJson.append({'AdresSieciDec':AdresSieciDec})
    TabToJson.append({'KlasaSieci':KlasaSieci})
    TabToJson.append({'MaskaSieciBin': MaskaSieciBin})
    TabToJson.append({'MaskaSieciDec': MaskaSieciDec})
    TabToJson.append({'AdresBroadcastBin': BroadcastBin})
    TabToJson.append({'AdresBroadcastDec': BroadcastDec})
    TabToJson.append({'PierwszyAdresBin': PierwszyHostBin})
    TabToJson.append({'PierwszyAdresDec': PierwszyHostDec})
    TabToJson.append({'OstatniAdresBin': OstatniHostBin})
    TabToJson.append({'OstatniAdresDec': OstatniHostDec})
    TabToJson.append({'MaxIloscHostowBin': MaxLiczbaHostowBin})
    TabToJson.append({'MaxIloscHostowDec': MaxLiczbaHostowDec})

    with open ('data.txt', 'w') as outfile:
        json.dump(TabToJson, outfile)
else:
    print("Adres nie jest prawidlowy")

