import React from 'react'
import PropTypes from 'prop-types'


function renderTitle(data, classes) {
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
const ProsesNer = props => {
    const {data,classes} = props
    return (
        <div className={classes.rootTitleText}>
            <p>Keyword : </p> 
            <div className={classes.rootTitleText}>
                {data && data.keywords.map(d2 => {
                    return renderTitle(d2, classes)
                })}
            </div>
        </div>
    )
}

ProsesNer.propTypes = {

}

export default ProsesNer
