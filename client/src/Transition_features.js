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
        const res = await axios.get('/api/transition_features')
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
            <div >
                <table className="dataframe">
                    <thead>
                        <tr>
                            <th>
                                From \ To
                            </th>
                            {result.map(x =>{
                                return x[0]
                            }).filter(onlyUnique).map(b => {
                                return (
                                    <th>
                                        {b}
                                    </th>
                                )
                            })}
                        </tr>
                    </thead>
                    <tbody>
                        {result.map(x => {
                            return x[0]
                        }).filter(onlyUnique).map(b => {
                            return (
                                <tr>
                                    <th>
                                        {b}
                                    </th>
                                    {result.map(x=>{
                                        return x
                                    }).filter(b2=>b2[0] == b).map(xx=>{
                                        return(
                                            <td>
                                                {xx[1]}
                                            </td>
                                        )
                                    })}
                                </tr>
                            )
                        })}
                    
                    </tbody>
                </table>
            </div>
        )
    }
}

export default Weights_target