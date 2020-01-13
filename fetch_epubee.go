package main

import (
        "encoding/json"
        "fmt"
        "github.com/antchfx/htmlquery"
        "io"
        "io/ioutil"
        "net/http"
        "net/http/cookiejar"
        "net/url"
        "os"
        "strings"
        "time"
)

type AutoGenerated struct {
        D []struct {
                Type        string `json:"__type"`
                ID          int    `json:"ID"`
                IsVip       int    `json:"isVip"`
                Name        string `json:"Name"`
                Email       string `json:"email"`
                KindleEmail string `json:"kindle_email"`
                UserName    string `json:"UserName"`
        } `json:"d"`
}

type AutoGenerated1 struct {
        D []string `json:"d"`
}

func main() {
        //      uid := "30324832"
        uid := "32328526"
        bid := `YEqb5zfd8o7XHjRXBH9gPVt2JQoSmMyAPCLcBjwP7cTZTiosWkHiuNb%2bpgoLfPBVER%2fmGlS3%2f3iszFdrKy707q%2f2YD3yRwfX5ftUKp6HhAzE1XaLH5SnNc1HK8aNwMprH%2baLPSc1cxZQIXHqTqAKjA%3d%3d`

        u, _ := url.Parse("http://cn.epubee.com/")

        cj, _ := cookiejar.New(nil)
        client := &http.Client{
                Jar: cj,
        }

        resp, err := client.Get("http://cn.epubee.com/")

        if err != nil {
                panic(err.Error())
        }

        body, err := ioutil.ReadAll(resp.Body)

        //fmt.Println(string(body))

        cookies := resp.Cookies()

        fmt.Println("xxxx")
        for _, cookie := range cookies {
                fmt.Println("cookie:", cookie.Name, ":", cookie.Value)
        }

        client.Jar.SetCookies(u, cookies)

        time.Sleep(1 * time.Second)

        var data string
        var req *http.Request

        /*
                data = `{localid:''}`
                req, _ = http.NewRequest("POST", "http://cn.epubee.com/keys/genid_with_localid.asmx/genid_with_localid", strings.NewReader(data))
                req.Header.Add("Content-Type", "application/json")

                resp, err = client.Do(req)
                body, err = ioutil.ReadAll(resp.Body)
                fmt.Println(string(body))
        */
        data = `{"d":[{"__type":"Container.json_Add_Temp","ID":32328526,"isVip":0,"Name":"ip_101.198.192.11","email":"","kindle_email":"","UserName":""}]}`
        //data = string(body)

        fmt.Println(data)

        p := &AutoGenerated{}
        err = json.Unmarshal([]byte(data), p)
        fmt.Println(err)

        fmt.Println((*p).D[0].ID)
        uid = fmt.Sprintf("%d", (*p).D[0].ID)
        fmt.Println(uid)
        user_localid := (*p).D[0].Name

        var clist []*http.Cookie
        clist = append(clist, &http.Cookie{
                Name:    "identify",
                Domain:  "cn.epubee.com",
                Path:    "/",
                Value:   uid,
                Expires: time.Now().AddDate(1, 0, 0),
        })
        clist = append(clist, &http.Cookie{
                Name:    "user_localid",
                Domain:  "cn.epubee.com",
                Path:    "/",
                Value:   user_localid,
                Expires: time.Now().AddDate(1, 0, 0),
        })

        client.Jar.SetCookies(u, clist)

        fmt.Println("cookie: %v", client.Jar.Cookies(u))

        resp, err = client.Get("http://cn.epubee.com/files.aspx?sortkey=&sort=&menukey=format&menuvalue=.mobi&skeyinput=&iskindle=0&aff=0&prom=0")
        //body, err = ioutil.ReadAll(resp.Body)
        //fmt.Println(string(body))

        cookies = resp.Cookies()
        fmt.Println("cookie: %v", cookies)

        clist = append(clist, &http.Cookie{
                Name:    "messagescount",
                Domain:  "cn.epubee.com",
                Path:    "/",
                Value:   "0",
                Expires: time.Now().AddDate(1, 0, 0),
        })

        client.Jar.SetCookies(u, clist)

        time.Sleep(1 * time.Second)

        doc, err := htmlquery.Parse(resp.Body)
        list, err := htmlquery.QueryAll(doc, `//a[@id="gvBooks_gvBooks_child_0_hpdownload_0"]`)
        fmt.Printf("%s", htmlquery.InnerText(list[0]))
        fmt.Printf("%s", htmlquery.SelectAttr(list[0], "target"))
        bid = fmt.Sprintf("%s", htmlquery.SelectAttr(list[0], "target"))

        data = `{isVip:0,uid:` + uid + `,strbid:'` + bid + `'}`
        req, _ = http.NewRequest("POST", "http://cn.epubee.com/app_books/click_key.asmx/getkey", strings.NewReader(data))
        req.Header.Add("Content-Type", "application/json")
        req.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
        req.Header.Add("Referer", "http://cn.epubee.com/files.aspx")
        resp, err = client.Do(req)
        body, err = ioutil.ReadAll(resp.Body)
        fmt.Println("------------\n")
        fmt.Println(string(body))

        time.Sleep(1 * time.Second)

        p1 := &AutoGenerated1{}
        err = json.Unmarshal([]byte(body), p1)
        fmt.Println((*p1).D[0])

        if (*p1).D[0] == "timeout" {
                panic("timeout")
        }

        url := "http://files.epubee.com/getFile.ashx?bid=" + bid + "&uid=" + uid + "&t_key=" + (*p1).D[0]

        fmt.Println(url)

        req, err = http.NewRequest("POST", url, nil)
        resp, err = client.Do(req)

        if err != nil {
                panic(err)
        }
        f, err := os.Create("/home/fengxin/aaaa.mobi")
        if err != nil {
                panic(err)
        }
        io.Copy(f, resp.Body)

}