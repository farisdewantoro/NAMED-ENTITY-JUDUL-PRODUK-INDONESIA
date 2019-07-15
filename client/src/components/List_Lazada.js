import React from 'react'
import PropTypes from 'prop-types'
import {Card, CardContent, Button} from '@material-ui/core'
// "TYPE": "TYPE", # 2119 "BRAND": "BRAND", # 1099 "NAME": "NAME", # 733
// "COLOR": "COLOR", # 414 "MATERIAL": "MATERIAL", # 202 "THEME": "THEME", # 161
// "DIMENSION": "DIMENSION", # 148 "GENDER": "GENDER", # 140 "SIZE": "SIZE", #
// 122 "MASS": "MASS", # 95 "AGE": "AGE", # 74 "SHAPE": "SHAPE", # 30
// "CAPACITY": "CAPACITY", # 52 "RAM": "RAM", # 24 "OS": "OS", # 15 "PROCESSOR":
// "PROCESSOR", # 14 "GRAPHIC": "GRAPHIC", # 7 "STORAGE": "STORAGE", # 7
// "DISPLAY": "DISPLAY", # 5 "MEMORY": "MEMORY", # 5 "CPU": "CPU", # 4 "CAMERA":
// "CAMERA", # 4
function renderTitle(data, classes) {
    let keys = Object.keys(data)
    let element =  keys.map(key=>{

        return (
            <li style={{display:'grid'}}>
                <span className={key}>
                    {data[key]}
                </span>
                <span className={classes.object_class}>
                    {key}
                </span>
            </li>
        )
    })
   return element
}

const List_Lazada = props => {

    const {classes, data, handlerStopCrawling} = props;
    const NoImg = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg' +
            '/480px-No_image_available.svg.png'

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
                <div
                    className='table-responsive'
                    style={{
                    maxHeight: 400
                }}>
                    <table className="table">
                        <tbody>
                            {data
                                .product_lazada
                                .map((d1, i) => {
                                    return (
                                        <tr >

                                            <td className={classes.rootTitleText}>
                                                {d1 && d1.named_tag.map(d2=>{
                                                    return  renderTitle(d2, classes)
                                                })}


                                            </td>

                                        </tr>
                                    )

                                })}
                        </tbody>
                        {/* <thead>
                            <tr>
                                <th>
                                    NO
                      </th>
                                <th>
                                    TITLE
                      </th>
                                <th>
                                    PRICE
                      </th>
                                <th>
                                    LOCATION
                      </th>
                            </tr>
                        </thead> */}
                        {/* <tbody>
                            {data.product_lazada.map((d, i) => {
                                return (
                                    <tr onClick={()=>window.open(d.link,'_blank')}>
                                        <td>
                                            {i + 1}
                                        </td>
                                        <td>
                                            {d.title}
                                        </td>
                                        <td>
                                            {d.price_now}
                                            <br />
                                            <del>
                                                {d.discount_price} &nbsp; {d.discount_percent}
                                            </del>

                                        </td>
                                        <td>
                                            {d.location}
                                        </td>
                                    </tr>
                                )
                            })}
                        </tbody> */}

                    </table>

                </div>
            </CardContent>
        </Card>

    )
}

List_Lazada.propTypes = {}

export default List_Lazada
