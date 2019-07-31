import React from 'react'
import PropTypes from 'prop-types'
import {Card, CardContent, Button,Grid} from '@material-ui/core'
import InfiniteScroll from 'react-infinite-scroller';

function renderTitle(data, classes) {
    let keys = Object.keys(data)
    let element =  data.map(key=>{

        return (
            <li style={{display:'grid'}}>
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
function renderDetail(data, classes) {

    let keys = Object.keys(data)
    let element = data.map(key => {

        if (key[0] !== 'O') {
            return (
                <mark data-entity={key[0]} className={key[0]}>
                    {key[1]}
                </mark>
            )
        } else {
            return ` ${key[1]} `
        }
    })
    return element
}

const List_Lazada = props => {

    const { classes, data, handlerStopCrawling, hasMoreData, loadFunc} = props;
    const NoImg = 'http!s://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg' +
            '/480px-No_image_available.svg.png'
    let data_dumy = {
        title: "Promo Notebook Baru Asus A407MA-BV001T - Intel® Celeron® N4000 - RAM 4GB - 1TB - Intel UHD Graphics 600 - 14.0' - W10 - Grey - Laptop Murah (Gratis Tas) - Bergansi",
        price_now: "Rp3.909.000",
        location: "Jawa barat",
        discount_price: "Rp195.000",
        discount_percent: "-31%",
        img_link: "https://id-live-01.slatic.net/original/ddec71a6c64fc3d46b4f22cfc5466008.jpg",
        link: "https://www.lazada.co.id/products/denim-original-hitam-i143570579-s157343054.html?search=1"
    }
    return (

        <Card>
            <CardContent>
                <div>
                    <h1
                        className={classes.titleProductRoot}
                        style={{
                        textAlign: 'left',
                        padding: '15px 0'
                    }}>
                        Total produk : {data.product_lazada_length}
                    </h1>
                </div>
                <div>

                    <div>
                        {data
                            .product_lazada
                            .map((d1, i) => {
                                return (
                                    <Card style={{marginTop:5}}>
                                        <CardContent>

                                            <Grid container direction="row" spacing={8}>
                                                <Grid item xs={4}>
                                                    <img src={d1.img_link} style={{
                                                        maxWidth: "100%"
                                                    }} alt="" />
                                                </Grid>
                                                <Grid item xs={8}>
                                                    <section className={classes.sectionProductTitle} onClick={() => window.open(d1.link, '_blank')}>
                                                        {d1 && d1.named_tag.map(d2 => {
                                                            return renderDetail(d2, classes)
                                                        })}


                                                    </section>
                                                    <div>
                                                        <h4>{d1.price}</h4>
                                                        <h4>{d1.location}</h4>
                                                    </div>
                                                </Grid>
                                            </Grid>

                                        </CardContent>

                                    </Card>
                                )

                            })}
                 
                    </div>
                </div>
                 {/* <div
                    className='table-responsive'
                    style={{
                        height:300,
                        overflow:'auto'
                    }}
                    >
               
                    <table className="table">
                        <tbody>
                       
                                
                            {data
                                .product_lazada
                                .map((d1, i) => {
                                    return (
                                        <tr >

                                            <td className={classes.rootTitleText} onClick={() => window.open(d1.link,'_blank')}>
                                                {d1 && d1.named_tag.map(d2=>{
                                                    return  renderTitle(d2, classes)
                                                })}


                                            </td>

                                        </tr>
                                    )

                                })}

                        
                        </tbody>
                   

                    </table>
                </div>  */}
            </CardContent>
        </Card>

    )
}

List_Lazada.propTypes = {}

export default List_Lazada
