import {Component} from 'inferno';
import ServerApi from '../../api';
import styles from './styles.module.scss';

export default class Docs extends Component {
  constructor(props) {
    super(props);
    this.state = {
      apiInfo: []
    };
  }

  componentDidMount() {
    ServerApi
      .fetchApiDoc()
      .then(json => {
        for(let i = 0; i < json.length; i++) {
          for(let j = 0; j < json[i].methods.length; j++) {
            // Do some rudimentary formatting of the description
            // There's probably a better way of doing this
            let splitString = json[i].methods[j].description.split('\n\n');
            let jsx = (
              <p>
                {
                  splitString.map((str, index) => 
                    <span>{str}<br /><br /></span>
                  )
                }
              </p>
            );
            json[i].methods[j].description=jsx;
          }
        }

        this.setState({...this.state, ...{apiInfo: json}});
      })
      .catch(err => console.error(err));
  }
  
  render() {
    return (
      <div>
        <h2>Developer documentation</h2>
        <p>This page documents the API endpoints available for developer use.</p>
        {
          this.state.apiInfo.map((doc, index) =>
            <div>
              <h3>{doc.route}</h3>
              {
                doc.methods.map((method, innerIndex) =>
                  <div className={styles.method}>
                    <h4><em>{method.method}</em></h4>
                    {method.description}
                  </div>
                )
              }
              <hr />
            </div>
          )
        }

      </div>
    );
  }
}