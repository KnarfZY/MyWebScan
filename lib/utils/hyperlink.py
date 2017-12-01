#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.core.common import getResponse
from urlparse import urlparse
from urlparse import urljoin
from lxml import html
from lib.core.settings import headers
def hyperLink(url,link=True,css=False,js=False,host=False):
    try:
        linklist=[]
        url=url if urlparse(url).scheme!="" else "http://"+url
        localstring =""

        resp=getResponse(url)
        try:
            page = html.fromstring(resp.read().decode('utf-8'))
        except:
            try:
                page = html.fromstring(getResponse(url).read().decode("gb2312"))
            except:
                page = html.fromstring(getResponse(url).read().decode((resp.info().getparam("charset")).upper()))
        if host:
            localstring=getUrlSource(url)
        if css and link:
            hrefs=page.xpath(u"//a|//link")
        elif link:
            hrefs = page.xpath(u"//a")
            for href in hrefs:
                if href.attrib.has_key('href'):
                    hreflink = href.attrib['href']
                    hreflink = urljoin(url, hreflink)
                    if host:
                        if localstring == getUrlSource(hreflink):
                            linklist.append(hreflink)

                    else:
                        linklist.append(hreflink)
        elif css:
            hrefs = page.xpath(u"//link")
            for href in hrefs:
                if  href.attrib.has_key('href'):
                    hreflink=href.attrib['href']
                    hreflink=urljoin(url,hreflink)
                    if host:
                        if localstring == getUrlSource(hreflink):
                            linklist.append(hreflink)

                    else:
                        linklist.append(hreflink)
        if js:
            srcs = page.xpath(u"//script")
            for src in srcs:
                #print dir(src),src.text
                if src.attrib.has_key('src'):
                    srclink = src.attrib['src']
                    srclink = urljoin(url, srclink)
                    if host:
                        if localstring == getUrlSource(srclink):
                            linklist.append(srclink)
                    else:
                        linklist.append(srclink)
        return linklist
    except:
        return []
def getUrlSource(url):
    try:
        url = url if urlparse(url).scheme != "" else "http://" + url
        # 这是国家级域名后缀字符串，如果有新增加，请按照“后缀-说明"的格式添加
        country_domain_names = """ad-Andorra安道尔
        ae-United Arab Emirates阿联酋
        af-Afghanistan阿富汗
        ag-Antigua and Barbuda安提瓜和巴布达
        ai-Anguilla安圭拉
        al-Albania阿尔巴尼亚
        am-Armenia亚美尼亚
        an-Netherlands Antilles荷兰属地
        ao-Angola安哥拉
        aq-Antarctica南极洲
        ar-Argentina阿根廷
        as-American Samoa东萨摩亚
        at-Austria奥地利
        au-Australia澳大利亚
        aw-Aruba阿鲁巴
        az-Azerbaijan阿塞拜疆
        ba-Bosnia Herzegovina波黑
        bb-Barbados巴巴多斯
        bd-Bangladesh孟加拉
        be-Belgium比利时
        bf-Burkina Faso布基纳法索
        bg-Bulgaria保加利亚
        bh-Bahrain巴林
        bi-Burundi布隆迪
        bj-Benin贝宁
        bm-Bermuda百慕大
        bn-Brunei Darussalam文莱
        bo-Bolivia玻利维亚
        br-Brazil巴西
        bs-Bahamas巴哈马
        bt-Bhutan不丹
        bv-Bouvet Island布韦岛
        bw-Botswana伯兹瓦纳
        by-Belarus白俄罗斯
        bz-Belize伯利兹
        ca-Canada加拿大
        cc-Cocos Islands科科斯群岛
        cf-Central African Republic中非
        cg-Congo刚果
        ch-Switzerland瑞士
        ci-Ivory Coast象牙海岸
        ck-Cook Islands库克群岛
        cl-Chile智利
        cm-Cameroon喀麦隆
        cn-China中国
        co-Colombia哥伦比亚
        cq-Equatorial Guinea赤道几内亚
        cr-Costa Rica哥斯达黎加
        cu-Cuba古巴
        cv-Cape Verde佛得角
        cx-Christmas Island圣诞岛(英属)
        cy-Cyprus塞浦路斯
        cz-Czech Republic捷克
        de-Germany德国
        dj-Djibouti吉布提
        dk-Denmark丹麦
        dm-Dominica多米尼加联邦
        do-Dominican Republic多米尼加
        dz-Algeria阿尔及利亚
        ec-Ecuador厄瓜多尔
        ee-Estonia爱沙尼亚
        eg-Egypt埃及
        eh-Western Sahara西萨摩亚
        es-Spain西班牙
        et-Ethiopia埃塞俄比亚
        ev-El Salvador萨尔瓦多
        fi-Finland芬兰
        fj-Fiji斐济
        fk-Falkland Islands福克兰群岛
        fm-Micronesia密克罗尼西亚
        fo-Faroe Islands法罗群岛
        fr-France法国
        ga-Gabon加蓬
        gb-Great Britain (UK)大不列颠联合王国
        gd-Grenada格林纳达
        ge-Georgia格鲁吉亚
        gf-French Guiana法属圭亚那
        gh-Ghana加纳
        gi-Gibraltar直布罗陀
        gl-Greenland格陵兰群岛
        gm-Gambia冈比亚
        gn-Guinea几内亚
        gp-Guadeloupe瓜德罗普岛(法属)
        gr-Greece希腊
        gt-Guatemala危地马拉
        gu-Guam关岛
        gw-Guinea-Bissau几内亚比绍
        gy-Guyana圭亚那
        hk-Hong Kong香港
        hm-Heard 赫德与麦克唐纳群岛
        hn-Honduras洪都拉斯
        hr-Croatia克罗地亚
        ht-Haiti海地
        hu-Hungary匈牙利
        id-Indonesia印度尼西亚
        ie-Ireland爱尔兰
        il-Israel以色列
        in-India印度
        io-British Indian Ocean Territory英属印度洋领地
        iq-Iraq伊拉克
        ir-Iran伊朗
        is-Iceland冰岛
        it-Italy意大利
        jm-Jamaica牙买加
        jo-Jordan约旦
        jp-Japan日本
        ke-Kenya肯尼亚
        kg-Kyrgyz Stan吉尔吉斯斯坦
        kh-Cambodia柬埔塞
        ki-Kiribati基里巴斯
        km-Comoros科摩罗
        kn-St. Kitts 圣基茨和尼维斯
        kp-Korea-North朝鲜
        kr-Korea-South韩国
        kw-Kuwait科威特
        ky-Cayman Islands开曼群岛(英属)
        kz-Kazakhstan哈萨克斯坦
        la-Lao People's Republic老挝
        lb-Lebanon黎巴嫩
        lc-St. Lucia圣露西亚岛
        li-Liechtenstein列支敦士登
        lk-Sri Lanka斯里兰卡
        lr-Liberia利比里亚
        ls-Lesotho莱索托
        lt-Lithuania立陶宛
        lu-Luxembourg卢森堡
        lv-Latvia拉脱维亚
        ly-Libya利比亚
        ma-Morocco摩洛哥
        mc-Monaco摩纳哥
        md-Moldova摩尔多瓦
        mg-Madagascar马达加斯加
        mh-Marshall Islands马绍尔群岛
        ml-Mali马里
        mm-Myanmar缅甸
        mn-Mongolia蒙古
        mo-Macao澳门
        mp-Northern Mariana Islands北马里亚纳群岛
        mq-Martinique马提尼克岛(法属)
        mr-Mauritania毛里塔尼亚
        ms-Montserrat蒙塞拉特岛
        mt-Malta马尔他
        mv-Maldives马尔代夫
        mw-Malawi马拉维
        mx-Mexico墨西哥
        my-Malaysia马来西亚
        mz-Mozambique莫桑比克
        na-Namibia纳米比亚
        nc-New Caledonia新喀里多尼亚
        ne-Niger尼日尔
        nf-Norfolk Island诺福克岛
        ng-Nigeria尼日利亚
        ni-Nicaragua尼加拉瓜
        nl-Netherlands荷兰
        no-Norway挪威
        np-Nepal尼泊尔
        nr-Nauru瑙鲁
        nt-Neutral Zone中立区
        nu-Niue纽埃
        nz-New Zealand新西兰
        om-Oman阿曼
        pa-Panama巴拿马
        pe-Peru秘鲁
        pf-French Polynesia法属玻利尼西亚
        pg-Papua New Guinea巴布亚新几内亚
        ph-Philippines菲律宾
        pk-Pakistan巴基斯坦
        pl-Poland波兰
        pm-St. Pierre 圣皮埃尔和密克隆群岛
        pn-Pitcairn Island皮特克恩岛
        pr-Puerto Rico波多黎各
        pt-Portugal葡萄牙
        pw-Palau帕劳
        py-Paraguay巴拉圭
        qa-Qatar卡塔尔
        re-Reunion Island留尼汪岛(法属)
        ro-Romania罗马尼亚
        ru-Russian Federation俄罗斯
        rw-Rwanda卢旺达
        sa-Saudi Arabia沙特阿拉伯
        sb-Solomon Islands所罗门群岛
        sc-Seychelles塞舌尔
        sd-Sudan苏旦
        se-Sweden瑞典
        sg-Singapore新加坡
        sh-St. Helena海伦娜
        si-Slovenia斯洛文尼亚
        sj-Svalbard 斯瓦尔巴特和扬马延岛
        sk-Slovakia斯洛伐克
        sl-Sierra Leone塞拉利昂
        sm-San Marino圣马力诺
        sn-Senegal塞内加尔
        so-Somalia索马里
        sr-Suriname苏里南
        st-Sao Tome 圣多美和普林西比
        su-USSR苏联
        sy-Syrian Arab Republic叙利亚
        sz-Swaziland斯威士兰
        tc-Turks 特克斯和凯科斯群岛
        td-Chad乍得
        tf-French Southern Territories法属南半球领地
        tg-Togo多哥
        th-Thailand泰国
        tj-Tajikistan塔吉克斯坦
        tk-Tokelau托克劳群岛
        tm-Turkmenistan土库曼斯坦
        tn-Tunisia突尼斯
        to-Tonga汤加
        tp-East Timor东帝汶
        tr-Turkey土耳其
        tt-Trinidad 特立尼达和多巴哥
        tv-Tuvalu图瓦鲁
        tw-Taiwan台湾
        tz-Tanzania坦桑尼亚
        ua-Ukrainian SSR 乌克兰
        ug-Uganda乌干达
        uk-United Kingdom英国
        us-United States美国
        uy-Uruguay乌拉圭
        va-Vatican City State梵地冈
        vc-St.Vincent 圣文森特和格林纳丁斯
        ve-Venezuela委内瑞拉
        vg-Virgin Islands维京群岛
        vn-Vietnam越南
        vu-Vanuatu瓦努阿图
        wf-Wallis 瓦利斯和富图钠群岛
        ws-Samoa西萨摩亚
        ye-Yemen也门
        yu-Yugoslavia南斯拉夫
        za-South Africa南非
        zm-Zambia赞比亚
        zr-Zaire扎伊尔
        zw-Zimbabwe津巴布韦"""
        # 这是国际级域名后缀字符串，如果有新增加，请按照“后缀-说明"的格式添加
        international_domain_names = """
        com-商业机构,任何人都可以注册
        edu-教育机构
        gov-政府部门
        int-国际组织
        mil-美国军事部门
        net-网络组织,例如因特网服务商和维修商,现在任何人都可以注册
        org-非盈利组织,任何人都可以注册
        biz-商业
        info-网络信息服务组织
        pro-用于会计、律师和医生
        name-用于个人
        museum-用于博物馆
        coop-用于商业合作团体
        aero-用于航空工业
        xxx-用于成人、色情网站
        idv-用于个人"""
        last_1 = map(lambda s: s.split("-")[0].strip(), country_domain_names.split("\n"))
        all_domain_names=[]
        last_2 = map(lambda s: s.split("-")[0].strip(), international_domain_names.split("\n"))
        all_domain_names=all_domain_names+last_1
        all_domain_names=all_domain_names+last_2
        for last2  in last_2:
            for last1 in last_1:
                all_domain_names.append(last2+'.'+last1)
        urlhost=urlparse(url).hostname
        dot_split=urlhost.split(".")
        if dot_split[-2]+"."+dot_split[-1] in all_domain_names :
            return dot_split[-3]
        elif dot_split[-1] in all_domain_names:
            return dot_split[-2]
        else :
            return False
    except:
        return False
