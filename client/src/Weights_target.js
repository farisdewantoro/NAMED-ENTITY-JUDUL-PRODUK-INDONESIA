import React, { Component } from 'react'
import PropTypes from 'prop-types'
import axios from 'axios'
function onlyUnique(value, index, self) {

    return self.indexOf(value) === index;
}
class Weights_target extends Component {
    state={
        result:[]
    }
    async componentDidMount(){
       try{
         const res =  await axios.get('/api/weights/targets')
         this.setState({
             result:res.data
         })
       }
       catch(err){
           console.log(err)
       }
    }

    render() {
        const { result} = this.state;
        return (
            <div  >
                <table className="dataframe" >
                    <thead>
                        <tr>
                            {result.map(x => {
                                return x[0]
                            }).filter(onlyUnique).map(b => {
                                return (
                                    <th style={{ textAlign: "center" }}>
                                        {b}
                                    </th>
                                )
                            })}
                        </tr>
                    </thead>
                    <tbody>
               
                                <tr>
                            {result.map(x => {
                                return x[0]
                            }).filter(onlyUnique).map(b => {
                                return (
                                            <td>
                                                <div>
                                                    <table >
                                                        <thead>
                                                            <tr>
                                                                <th style={{
                                                                    background:"None",
                                                                    color:"black",
                                                                    textAlign:"center"
                                                                }}>
                                                                    Weight
                                                            </th>
                                                                <th style={{
                                                                    background:"None",
                                                                    color:"black",
                                                                    textAlign:"center"
                                                                }}>
                                                                    Featrue
                                                            </th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                    {result.map(x => {
                                                        return x
                                                    }).filter(b2 => b2[0] == b).map(xx => {
                                                        return (
                                                            <tr>
                                                                <td>
                                                                    {xx[2]}
                                                                </td>
                                                                <td>
                                                                    {xx[1]}
                                                                </td>
                                                            </tr>
                                                                   )
                             })}
                                                        </tbody>
                                                    </table>
                                                </div>
                                               
                                                {/* <ul>
                                                    <li>
                                                      
                                                    </li>
                                                    <li>
                                                        
                                                    </li>
                                                </ul> */}
                                          
                                            </td>
                                )
                            })}
                                </tr>
                    

                    </tbody>
                </table>
            </div>
        )
    }
}

export default Weights_target