import React,{Fragment} from 'react'
import PropTypes from 'prop-types'
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import {
    Card,
    CardContent
} from '@material-ui/core'
const Summary = props => {
    const [expanded, setExpanded] = React.useState(false);
    const {classes,data} = props;
    const handleChange = panel => (event, isExpanded) => {
        setExpanded(isExpanded ? panel : false);
    };
  
    return (
        <Fragment>
            <Card>
                <CardContent>
            <div>
                        <h1
                            className={classes.titleProductRoot}
                            style={{
                                textAlign: 'left',
                                padding: '15px 0'
                            }}>
                            Report : 
                        </h1>
            </div>
           {Object.keys(data.summary).map(d=>{
               return(
                   <ExpansionPanel expanded={expanded === d} key={d} onChange={handleChange(d)}>
                       <ExpansionPanelSummary
                           expandIcon={<ExpandMoreIcon />}
                           aria-controls={"panel-"+d}
                           id={"panel1bh-header"+d}
                       >
                           <div className={classes.listPanel}>
                               <Typography className={classes.heading}>{d}</Typography>
                               {data.summary[d].values.length > 0 && (
                                   <Fragment>
                                       <div style={{padding:"0px 10px"}}>
                                           <p className={classes.secondaryHeading}>Entitas terbanyak : </p>
                                           <p className={data.summary[d].values[0].bio}>{data.summary[d].values.length > 0 && data.summary[d].values[0].bio} :  {data.summary[d].values.length > 0 && data.summary[d].values[0].name}  </p>
                                           <p className={classes.secondaryHeading}> Total : {data.summary[d].values.length > 0 && data.summary[d].values[0].value}</p>
                                       </div>
                                       <p className={classes.secondaryHeading}> Total keseluruhan : {data.summary[d].values.length+1}  </p>
                                   </Fragment>
                                 
                               )}
                            </div>

                       </ExpansionPanelSummary>
                       <ExpansionPanelDetails>
                           <div>
                           <Typography>
                               {data.summary[d].description}
                           </Typography>
                               <ol>
                               {data.summary[d].values.map(d2=>{
                             
                                       
                                   return(
                                       <li key={d2.bio+d2.name}>
                                           {d2.bio} : {d2.name} &nbsp;&nbsp;&nbsp;-&nbsp;&nbsp; {d2.value}
                                       </li>
                                   )
                                   
                               })}
                           
                                   </ol>
                           </div>
                       </ExpansionPanelDetails>
                   </ExpansionPanel>
               )
           })}
         
        
         
          
                </CardContent>
            </Card>
        </Fragment>
    )
}

Summary.propTypes = {

}

export default Summary
