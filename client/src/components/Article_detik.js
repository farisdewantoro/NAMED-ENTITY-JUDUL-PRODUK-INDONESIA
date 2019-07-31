import React, { Fragment } from 'react'
import PropTypes from 'prop-types'
import { Card, CardContent, Button } from '@material-ui/core'

const dummy = [{ "judul": "Usai Prabowo, Jokowi Belum Ada Rencana Bertemu SBY", "date": "Minggu 28 Juli 2019, 13:41 WIB", "img": "https://akcdn.detik.net.id/community/media/visual/2019/07/28/7bd7e59f-581f-4910-92ef-c26a290607b0.jpeg?w=780&q=90", "detail": [[["B-ORG", "Solo"], ["I-ORG", "Partai"], ["I-ORG", "Demokrat"], ["B-ORG", "PD"], ["O", "mengatakan"], ["O", "ada"], ["O", "kemungkinan"], ["O", "Ketua"], ["O", "Umum"], ["O", "PD"], ["B-PER", "Susilo"], ["I-PER", "Bambang"], ["I-PER", "Yudhoyono"], ["B-PER", "SBY"], ["O", "akan"], ["O", "bertemu"], ["O", "dengan"], ["O", "Presiden"], ["B-PER", "Joko"], ["I-PER", "Widodo"], ["B-PER", "Jokowi"], ["O", "dalam"], ["O", "waktu"], ["O", "dekat"], ["O", "Namun"], ["B-PER", "Jokowi"], ["O", "sendiri"], ["O", "mengatakan"], ["O", "belum"], ["O", "ada"], ["O", "rencana"], ["O", "tersebut"], ["B-ORG", "Belum"], ["I-ORG", "Belum"], ["I-ORG", "Belum"], ["O", "ada"], ["O", "rencana"], ["B-PER", "Jokowi"], ["O", "di"], ["B-LOC", "Restoran"], ["I-LOC", "Mbah"], ["I-LOC", "Karto"], ["I-LOC", "Sukoharjo"], ["B-LOC", "Jawa"], ["I-LOC", "Tengah"], ["O", "Minggu"], ["O", "28"], ["O", "7"], ["O", "2019"], ["O", "Meski"], ["O", "demikian"], ["B-PER", "Jokowi"], ["O", "menegaskan"], ["O", "pertemuan"], ["O", "dengan"], ["O", "siapapun"], ["O", "menjadi"], ["O", "penting"], ["O", "Termasuk"], ["O", "dengan"], ["B-PER", "SBY"], ["I-PER", "Baca"], ["O", "juga"], ["O", "Menanti"], ["O", "Pertemuan"], ["B-PER", "Jokowi"], ["B-PER", "SBY"], ["O", "dan"], ["O", "Isu"], ["O", "Kursi"], ["O", "Menteri"], ["O", "untuk"], ["B-ORG", "AHY"], ["I-ORG", "Ya"], ["O", "ketemu"], ["O", "dengan"], ["O", "siapa"], ["O", "pun"], ["O", "itu"], ["O", "penting"], ["O", "untuk"], ["O", "membangun"], ["O", "silaturahmi"], ["O", "Dengan"], ["O", "semua"], ["O", "katanya"], ["B-ORG", "Partai"], ["I-ORG", "Demokrat"], ["B-ORG", "PD"], ["O", "mengatakan"], ["B-PER", "Susilo"], ["I-PER", "Bambang"], ["I-PER", "Yudhoyono"], ["B-PER", "SBY"], ["O", "ada"], ["O", "kemungkinan"], ["O", "akan"], ["O", "segera"], ["O", "mengelar"], ["O", "pertemuan"], ["O", "dengan"], ["O", "sejumlah"], ["O", "tokoh"], ["O", "nasional"], ["O", "pasca"], ["O", "masa"], ["O", "berkabung"], ["O", "40"], ["O", "hari"], ["O", "meninggalnya"], ["O", "Ani"], ["O", "Yudhoyono"], ["B-ORG", "PD"], ["O", "mengatakan"], ["O", "kemungkinan"], ["O", "tokoh"], ["O", "yang"], ["O", "akan"], ["O", "ditemui"], ["O", "SBY"], ["O", "pertama"], ["O", "kali"], ["O", "ialah"], ["O", "presiden"], ["O", "terpilih"], ["B-PER", "Joko"], ["I-PER", "Widodo"], ["I-PER", "Tentu"], ["O", "akan"], ["O", "terjadi"], ["O", "komunikasi"], ["O", "komunikasi"], ["O", "dengan"], ["O", "pertama"], ["O", "tama"], ["O", "sekali"], ["O", "dengan"], ["O", "maksud"], ["O", "saya"], ["O", "dengan"], ["O", "presiden"], ["O", "terpilih"], ["B-PER", "Jokowi"], ["O", "dan"], ["O", "itu"], ["O", "diyakini"], ["O", "akan"], ["O", "dapat"], ["O", "dilakukan"], ["O", "tidak"], ["O", "dalam"], ["O", "waktu"], ["O", "yang"], ["O", "lama"], ["O", "lagi"], ["O", "sebut"], ["O", "Waketum"], ["O", "PD"], ["B-PER", "Syarief"], ["I-PER", "Hasan"], ["O", "dalam"], ["O", "diskusi"], ["O", "bertajuk"], ["B-PER", "Utak"], ["I-PER", "Atik"], ["B-PER", "Manuver"], ["I-PER", "Elite"], ["O", "di"], ["B-LOC", "Resto"], ["I-LOC", "D"], ["I-LOC", "Consulate"], ["B-LOC", "Jl"], ["I-LOC", "Wahid"], ["I-LOC", "Hasyim"], ["B-LOC", "Jakarta"], ["I-LOC", "Pusat"], ["O", "Sabtu"], ["O", "27"], ["O", "7"], ["O", "2019"], ["O", "Baca"], ["O", "juga"], ["O", "PD"], ["O", "Bicara"], ["O", "Rencana"], ["O", "Pertemuan"], ["O", "SBY"], ["B-PER", "Jokowi"], ["I-PER", "Mungkin"], ["O", "Awal"], ["O", "Agustus"], ["O", "Tak"], ["O", "hanya"], ["O", "dengan"], ["B-PER", "Jokowi"], ["I-PER", "Syarief"], ["O", "mengatakan"], ["B-PER", "SBY"], ["O", "juga"], ["O", "akan"], ["O", "bertemu"], ["O", "dengan"], ["O", "sejumlah"], ["O", "tokoh"], ["O", "lain"], ["O", "Menurutnya"], ["O", "sejalan"], ["O", "dengan"], ["O", "rencana"], ["O", "itu"], ["O", "kini"], ["B-ORG", "PD"], ["O", "mulai"], ["O", "menjalin"], ["O", "komunikasi"], ["O", "dengan"], ["B-ORG", "PDIP"], ["O", "ataupun"], ["B-PER", "Gerindra"], ["I-PER", "Kami"], ["O", "melakukan"], ["O", "komunikasi"], ["O", "dengan"], ["O", "semua"], ["O", "partai"], ["O", "partai"], ["O", "politik"], ["O", "sebelum"], ["O", "Pak"], ["B-PER", "SBY"], ["O", "melakukan"], ["O", "pertemuan"], ["O", "resmi"], ["O", "Dengan"], ["O", "teman"], ["O", "teman"], ["O", "dari"], ["B-ORG", "PDIP"], ["O", "juga"], ["O", "akan"], ["O", "dilakukan"], ["O", "dengan"], ["B-ORG", "Gerindra"], ["O", "juga"], ["O", "komunikasi"], ["O", "hampir"], ["O", "dipastikan"], ["O", "bahwa"], ["O", "bagi"], ["B-ORG", "Partai"], ["I-ORG", "Demokrat"], ["O", "posisi"], ["O", "mana"], ["O", "pun"], ["O", "kita"], ["O", "itu"], ["O", "komunikasi"], ["O", "harus"], ["O", "tetap"], ["O", "kita"], ["O", "jalin"], ["O", "dan"], ["O", "harus"], ["O", "kita"], ["O", "tingkatkan"], ["O", "sehingga"], ["O", "pada"], ["O", "saat"], ["O", "final"], ["O", "terakhir"], ["O", "itu"], ["O", "sangat"], ["O", "mudah"], ["O", "untuk"], ["O", "kita"], ["O", "mendapat"], ["O", "suatu"], ["O", "konsensus"], ["O", "bersama"], ["O", "ujarnya"], ["B-PER", "Jokowi"], ["O", "sendiri"], ["O", "sebelumnya"], ["O", "sudah"], ["O", "bertemu"], ["O", "dengan"], ["O", "mantan"], ["O", "rivalnya"], ["O", "di"], ["B-LOC", "Pilpres"], ["O", "2019"], ["O", "yakni"], ["B-PER", "Prabowo"], ["I-PER", "Subianto"], ["O", "pada"], ["O", "Sabtu"], ["O", "13"], ["O", "6"], ["O", "lalu"], ["O", "Pertemuan"], ["O", "keduanya"], ["O", "berlangsung"], ["O", "di"], ["B-LOC", "Stasiun"], ["I-LOC", "MRT"], ["B-LOC", "Jakarta"], ["O", "Tonton"], ["O", "video"], ["O", "Bertemu"], ["O", "Prabowo"], ["O", "Rachmawati"], ["O", "Ingin"], ["O", "Gerindra"], ["O", "Jadi"], ["O", "Oposisi"], ["O", "jor"], ["O", "tor"], ["O", "jokowi"], ["O", "birodiyjateng"], ["O", "sby"], ["O", "demokrat"], ["O", "Bagikan"], ["O", "Kontribusi"], ["O", "Seputar"], ["O", "Sosok"], ["O", "Menginspirasi"], ["O", "dan"], ["O", "Dapatkan"], ["O", "Ribuan"], ["O", "Poin"]]] }]

function renderTitle(data, classes) {
    console.log(data)
    let keys = Object.keys(data)
    let element = data.map(key => {

        return (
            <li style={{ display: 'grid' }}>
                <span className={key[0]}>
                    {key[1]}
                </span>
                <span className={classes.object_class}>
                    {key[0]}
                </span>
            </li>
        )
    })
    return element
}
function renderDetail(data,classes){
 
    let keys = Object.keys(data)
    let element = data.map(key => {
        console.log(key)
        if (key[0] !== 'O'){
            return (
                <mark data-entity={key[0]} className={key[0]}>
                    {key[1]}
                </mark>
            )
        }else{
            return ` ${key[1]} `
        }
     
        // return (
        //     <li style={{ display: 'grid' }} >
        //         <span className={key[0]}>
        //             {key[1]}
        //         </span>
        //         <span className={classes.object_class}>
        //             {key[0]}
        //         </span>
        //     </li>
        // )
    })
    return element
}
function scrollingFunc(e) {
    console.log('ada')
    console.log(e)
}

const List_Lazada = props => {

    const { classes, data,handlerStopCrawling, hasMoreData, loadFunc } = props;
    const NoImg = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg' +
        '/480px-No_image_available.svg.png'

    return (
        <div style={{padding:20}}>
            {/* {dummy.map(d=>{ */}
            {data.list_article.map(d => {
           
            return(
                <Fragment>
                  
                <Card>
                    <CardContent>
                        <div>
                            <span>{d.date}</span>
                            <h2>{d.judul}</h2>
                        </div>
                        <div>
                                {/* <div>
                                    <img src={d.img} className={classes.imgArtikel} alt="" />
                                </div> */}

                                <div>
                                    {d.detail
                                        .map((d2, i) => {
                                            return (
                                                <section className={classes.sectionArticle}>
                                                    {renderDetail(d2, classes)}
                                                </section>
                                            )

                                        })}
                                </div>
                        </div>
                       

                        {/* {data
                    .product_lazada
                    .map((d1, i) => {
                        return (
                            <tr >

                                <td className={classes.rootTitleText} onClick={() => window.open(d1.link, '_blank')}>
                                    {d1 && d1.named_tag.map(d2 => {
                                        return renderTitle(d2, classes)
                                    })}


                                </td>

                            </tr>
                        )

                    })} */}
                    </CardContent>
                </Card>

                </Fragment>
            )
        })}
      

        </div>
    )
}

List_Lazada.propTypes = {}

export default List_Lazada

