import React, { Fragment } from 'react'
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
    let data_dumy = [{ "title": "ACER A314-32-C3X0 - Intel CeleronN4000 - 4GB - 1TB - 14\" - W10 - Black - Laptop Murah (Gratis Tas) - Bergaransi", "link": "https://www.lazada.co.id/products/acer-a314-32-c3x0-intel-celeronn4000-4gb-1tb-14-w10-black-laptop-murah-gratis-tas-bergaransi-i466140285-s564742242.html?search=1", "location": "DKI Jakarta,Kota Jakarta Barat,Cengkareng", "price": "Rp3.899.000", "img_link": "https://id-test-11.slatic.net/p/4d10eb22143fccb0efdb0940a1ca1b6f.jpg_340x340q80.jpg", "named_tag": [[["B-BRAND", "ACER"], ["B-NAME", "A314"], ["I-NAME", "32"], ["I-NAME", "C3X0"], ["B-PROCESSOR", "Intel"], ["I-PROCESSOR", "CeleronN4000"], ["B-RAM", "4GB"], ["B-CAPACITY", "1TB"], ["O", "14"], ["B-NAME", "W10"], ["B-COLOR", "Black"], ["B-TYPE", "Laptop"], ["O", "Murah"], ["O", "Gratis"], ["O", "Tas"], ["O", "Bergaransi"]]], "text_extraction": { "BRAND": ["ACER"], "NAME": ["A314 32 C3X0", "W10"], "PROCESSOR": ["Intel CeleronN4000"], "RAM": ["4GB"], "CAPACITY": ["1TB"], "COLOR": ["Black"], "TYPE": ["Laptop"] } }]

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
                        {data.product_lazada
                            .map((d1, i) => {
                                return (
                                    <Card style={{marginTop:5}} key={i}>
                                        <CardContent>

                                            <Grid container direction="row" alignContent="center" alignItems="center" spacing={8}>
                                                <Grid item xs={4}>
                                                    <img src={d1.img_link} style={{
                                                        maxWidth: "100%"
                                                    }} alt="" />
                                                </Grid>
                                                <Grid item xs={8}>
                                                    <div>
                                                        <h3 className={classes.titleNormal} onClick={() => window.open(d1.link, '_blank')}>{d1.title}</h3>
                                                    </div>
                                                    <section className={classes.sectionProductTitle} onClick={() => window.open(d1.link, '_blank')}>
                                                        {d1 && d1.named_tag.map(d2 => {
                                                            return renderDetail(d2, classes)
                                                        })}


                                                    </section>
                                                    <ul>
                                                        {Object.keys(d1.text_extraction).map((k,i2)=>{
                                                            return(
                                                                <Fragment>
                                                                    <li key={i2} style={{padding:"2px 0px"}}>
                                                                        <span style={{
                                                                            fontWeight:"bold"
                                                                        }}> {k} </span>: {d1.text_extraction[k].map((val,i3) => {
                                                                            return (
                                                                                <span key={i3} style={{padding:'0px 5px'}}>
                                                                                    {val},
                                                                                </span>
                                                                            )
                                                                        })}
                                                                       
                                                                    
                                                                    </li>
                                                                </Fragment>
                                                            )
                                                        })}
                                                    </ul>
                                                    {/* <div>
                                                        <h4>{d1.price}</h4>
                                                        <h4>{d1.location}</h4>
                                                    </div> */}
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
