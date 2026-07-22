def calculate_50_sahams(
    lagna_spashta: float = 123.45,
    surya_spashta: float = 45.12,
    chandra_spashta: float = 78.33,
    mangal_spashta: float = 120.0,
    budh_spashta: float = 110.0,
    guru_spashta: float = 200.0,
    shukra_spashta: float = 250.0,
    shani_spashta: float = 300.0,
    varsha_lagna_spashta: float = 130.0,
    ashtam_bhav_madhya: float = 240.0,
    navam_bhav_madhya: float = 270.0,
    dwitiya_bhav_madhya: float = 150.0,
    shashtha_bhav_madhya: float = 210.0,
    ekadash_bhav_madhya: float = 330.0,
    surya_paramochcha: float = 10.0,
    chandra_paramochcha: float = 33.0
):
    # Exact Tajik formulas
    def add(a, b): return (a + b) % 360
    def sub(a, b): return (a - b) % 360

    sahams = {}
    
    # 1 Punya Saham
    saham1 = add(sub(chandra_spashta, surya_spashta), varsha_lagna_spashta)
    sahams[1] = {"name": "Punya Saham", "deg": saham1}
    
    # 2 Guru Saham
    saham2 = add(sub(surya_spashta, chandra_spashta), varsha_lagna_spashta)
    sahams[2] = {"name": "Guru Saham", "deg": saham2}
    
    # 3 Gyan Saham
    saham3 = add(sub(surya_spashta, chandra_spashta), varsha_lagna_spashta)
    sahams[3] = {"name": "Gyan Saham", "deg": saham3}
    
    # 4 Yash Saham
    saham4 = add(sub(guru_spashta, saham1), varsha_lagna_spashta)
    sahams[4] = {"name": "Yash Saham", "deg": saham4}
    
    # 5 Mitra Saham
    saham5 = add(sub(saham2, saham1), shukra_spashta)
    sahams[5] = {"name": "Mitra Saham", "deg": saham5}
    
    # 6 Mahatmya
    saham6 = add(sub(saham1, mangal_spashta), lagna_spashta)
    sahams[6] = {"name": "Mahatmya Saham", "deg": saham6}
    
    # 7 Asha
    saham7 = add(sub(shani_spashta, shukra_spashta), lagna_spashta)
    sahams[7] = {"name": "Asha Saham", "deg": saham7}
    
    # 8 Samarthya
    lagnesh_spashta = guru_spashta
    saham8 = add(sub(mangal_spashta, lagnesh_spashta), lagna_spashta)
    sahams[8] = {"name": "Samarthya Saham", "deg": saham8}
    
    # 9 Bhratri
    saham9 = add(sub(guru_spashta, shani_spashta), lagna_spashta)
    sahams[9] = {"name": "Bhratri Saham", "deg": saham9}
    
    # 10 Gaurav
    saham10 = add(sub(guru_spashta, chandra_spashta), surya_spashta)
    sahams[10] = {"name": "Gaurav Saham", "deg": saham10}
    
    # 11 Rajya
    saham11 = add(sub(shani_spashta, surya_spashta), lagna_spashta)
    sahams[11] = {"name": "Rajya Saham", "deg": saham11}
    
    # 12 Tat
    saham12 = saham11
    sahams[12] = {"name": "Tat Saham", "deg": saham12}
    
    # 13 Matri
    saham13 = add(sub(chandra_spashta, shukra_spashta), lagna_spashta)
    sahams[13] = {"name": "Matri Saham", "deg": saham13}
    
    # 14 Putra
    saham14 = add(sub(guru_spashta, chandra_spashta), lagna_spashta)
    sahams[14] = {"name": "Putra Saham", "deg": saham14}
    
    # 15 Jeevan
    saham15 = add(sub(shani_spashta, guru_spashta), lagna_spashta)
    sahams[15] = {"name": "Jeevan Saham", "deg": saham15}
    
    # 16 Jal
    saham16 = saham13
    sahams[16] = {"name": "Jal Saham", "deg": saham16}
    
    # 17 Karma
    saham17 = add(sub(mangal_spashta, budh_spashta), lagna_spashta)
    sahams[17] = {"name": "Karma Saham", "deg": saham17}
    
    # 18 Rog
    saham18 = add(sub(lagna_spashta, chandra_spashta), lagna_spashta)
    sahams[18] = {"name": "Rog Saham", "deg": saham18}
    
    # 19 Kam
    saham19 = add(sub(chandra_spashta, lagnesh_spashta), lagna_spashta)
    sahams[19] = {"name": "Kam Saham", "deg": saham19}
    
    # 20 Kali
    saham20 = add(sub(guru_spashta, mangal_spashta), lagna_spashta)
    sahams[20] = {"name": "Kali Saham", "deg": saham20}
    
    # 21 Kshama
    sahams[21] = {"name": "Kshama Saham", "deg": saham20}
    
    # 22 Shastra
    saham22 = add(sub(guru_spashta, shani_spashta), budh_spashta)
    sahams[22] = {"name": "Shastra Saham", "deg": saham22}
    
    # 23 Bandhu
    saham23 = add(sub(budh_spashta, chandra_spashta), lagna_spashta)
    sahams[23] = {"name": "Bandhu Saham", "deg": saham23}
    
    # 24 Bandak
    saham24 = add(sub(chandra_spashta, budh_spashta), lagna_spashta)
    sahams[24] = {"name": "Bandak Saham", "deg": saham24}
    
    # 25 Mrityu
    saham25 = add(sub(ashtam_bhav_madhya, chandra_spashta), shani_spashta)
    sahams[25] = {"name": "Mrityu Saham", "deg": saham25}
    
    # 26 Pardesh
    navamesh = guru_spashta
    saham26 = add(sub(navam_bhav_madhya, navamesh), lagna_spashta)
    sahams[26] = {"name": "Pardesh Saham", "deg": saham26}
    
    # 27 Dhan
    dwitiyesh = shukra_spashta
    saham27 = add(sub(dwitiya_bhav_madhya, dwitiyesh), lagna_spashta)
    sahams[27] = {"name": "Dhan Saham", "deg": saham27}
    
    # 28 Pardara
    saham28 = add(sub(shukra_spashta, surya_spashta), lagna_spashta)
    sahams[28] = {"name": "Pardara Saham", "deg": saham28}
    
    # 29 Parkarma
    saham29 = add(sub(chandra_spashta, shani_spashta), lagna_spashta)
    sahams[29] = {"name": "Parkarma Saham", "deg": saham29}
    
    # 30 Vanik
    saham30 = add(sub(chandra_spashta, budh_spashta), lagna_spashta)
    sahams[30] = {"name": "Vanik Saham", "deg": saham30}
    
    # 31 Karyasiddhi
    surya_rashi_sh = surya_spashta
    saham31 = add(sub(shani_spashta, surya_spashta), surya_rashi_sh)
    sahams[31] = {"name": "Karyasiddhi Saham", "deg": saham31}
    
    # 32 Vivah
    saham32 = add(sub(shukra_spashta, shani_spashta), lagna_spashta)
    sahams[32] = {"name": "Vivah Saham", "deg": saham32}
    
    # 33 Prasuti
    saham33 = add(sub(guru_spashta, budh_spashta), lagna_spashta)
    sahams[33] = {"name": "Prasuti Saham", "deg": saham33}
    
    # 34 Santap
    saham34 = add(sub(shani_spashta, chandra_spashta), shashtha_bhav_madhya)
    sahams[34] = {"name": "Santap Saham", "deg": saham34}
    
    # 35 Shraddha
    saham35 = add(sub(shukra_spashta, mangal_spashta), lagna_spashta)
    sahams[35] = {"name": "Shraddha Saham", "deg": saham35}
    
    # 36 Priti
    saham36 = add(sub(saham3, saham1), lagna_spashta)
    sahams[36] = {"name": "Priti Saham", "deg": saham36}
    
    # 37 Bal
    saham37 = add(sub(guru_spashta, saham1), varsha_lagna_spashta)
    sahams[37] = {"name": "Bal Saham", "deg": saham37}
    
    # 38 Deh
    sahams[38] = {"name": "Deh Saham", "deg": saham37}
    
    # 39 Jadya
    saham39 = add(sub(mangal_spashta, shani_spashta), budh_spashta)
    sahams[39] = {"name": "Jadya Saham", "deg": saham39}
    
    # 40 Vyapar
    saham40 = add(sub(mangal_spashta, budh_spashta), lagna_spashta)
    sahams[40] = {"name": "Vyapar Saham", "deg": saham40}
    
    # 41 Paniyapat
    saham41 = add(sub(shani_spashta, chandra_spashta), lagna_spashta)
    sahams[41] = {"name": "Paniyapat Saham", "deg": saham41}
    
    # 42 Shatru
    saham42 = add(sub(mangal_spashta, shani_spashta), lagna_spashta)
    sahams[42] = {"name": "Shatru Saham", "deg": saham42}
    
    # 43 Shaurya
    saham43 = add(sub(saham1, mangal_spashta), lagna_spashta)
    sahams[43] = {"name": "Shaurya Saham", "deg": saham43}
    
    # 44 Upay
    saham44 = add(sub(shani_spashta, guru_spashta), lagna_spashta)
    sahams[44] = {"name": "Upay Saham", "deg": saham44}
    
    # 45 Daridra
    saham45 = add(sub(budh_spashta, saham1), budh_spashta)
    sahams[45] = {"name": "Daridra Saham", "deg": saham45}
    
    # 46 Guruta
    saham46 = add(sub(surya_paramochcha, surya_spashta), lagna_spashta)
    sahams[46] = {"name": "Guruta Saham", "deg": saham46}
    
    # 47 Jalpath
    three_15 = 3 + 15 / 60
    saham47 = add(sub(three_15, shani_spashta), lagna_spashta)
    sahams[47] = {"name": "Jalpath Saham", "deg": saham47}
    
    # 48 Bandhan
    saham48 = add(sub(saham1, shani_spashta), lagna_spashta)
    sahams[48] = {"name": "Bandhan Saham", "deg": saham48}
    
    # 49 Kanya
    saham49 = add(sub(shukra_spashta, chandra_spashta), lagna_spashta)
    sahams[49] = {"name": "Kanya Saham", "deg": saham49}
    
    # 50 Ashwa
    saham50 = add(sub(saham1, surya_spashta), ekadash_bhav_madhya)
    sahams[50] = {"name": "Ashwa Saham", "deg": saham50}
    
    for i in range(1, 51):
        deg = sahams[i]["deg"]
        house = int(deg // 30) + 1
        shubh = house in [1, 2, 4, 5, 9, 10, 11]
        sahams[i]["house"] = house
        sahams[i]["shubh_ashubh"] = "Shubh" if shubh else "Ashubh"
        sahams[i]["deg_norm"] = round(deg, 2)
        
    return sahams
