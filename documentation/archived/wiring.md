### Wire configuration for final gizmo


<table>
  <tr>
    <th>System</th>
    <th>Element</th>
    <th>GPIO Pin</th>
    <th>BCM Pin</th>
    <th>Colour</th>
    <th>Purpose</th>
    <th>Connected to...</th>
  </tr>
  <tr>
    <td rowspan="3">SS1-2</td>
    <td>GRND</td>
    <td>14</td>
    <td>-</td>
    <td>Orange(1)</td>
    <td>Common ground</td>
    <td>GRND of SolenoidSystem 1&2</td>
  </tr>
  <tr>
    <td>S1</td>
    <td>13</td>
    <td>27</td>
    <td>Yellow(1)</td>
    <td>I/O Output</td>
    <td>Gate pin of transistor sol-1</td>
  </tr>
  <tr>
    <td>S2</td>
    <td>11</td>
    <td>17</td>
    <td>Blue(1)</td>
    <td>I/O Output</td>
    <td>Gate pin of transistor sol-2</td>
  </tr>
  <tr>
    <td rowspan="3">SS3-4</td>
    <td>GRND</td>
    <td>30</td>
    <td>-</td>
    <td>Purple(2)</td>
    <td>Common ground</td>
    <td>GRND of SolenoidSystem 3&4</td>
  </tr>
  <tr>
    <td>S3</td>
    <td>29</td>
    <td>5</td>
    <td>Grey(2)</td>
    <td>I/O Output</td>
    <td>Gate pin of transistor sol-3</td>
  </tr>
  <tr>
    <td>S4</td>
    <td>31</td>
    <td>6</td>
    <td>Blue(3)</td>
    <td>I/O Output</td>
    <td>Gate pin of transistor sol-4</td>
  </tr>
  <tr>
    <td>MS1/CS1</td>
    <td>GRND</td>
    <td>14</td>
    <td>-</td>
    <td>Orange(1)</td>
    <td>Common ground</td>
    <td>GRND of MotorSystem</td>
  </tr>
  <tr>
    <td>MS1</td>
    <td>MOT1</td>
    <td>12</td>
    <td>18</td>
    <td>Green(1)</td>
    <td>PWM Output</td>
    <td>Gate pin of transistor for motor</td>
  </tr>
  <tr>
    <td rowspan="2">CS1</td>
    <td>MS1</td>
    <td>16</td>
    <td>23</td>
    <td>Brown(1)</td>
    <td>I/O Input</td>
    <td>Microswitch pin 1</td>
  </tr>
  <tr>
    <td>LED</td>
    <td>18</td>
    <td>24</td>
    <td>White(1)</td>
    <td>I/O Output</td>
    <td>LED pin</td>
  </tr>
  <tr>
    <td rowspan="4">LS1</td>
    <td>GRND</td>
    <td>34</td>
    <td>-</td>
    <td>Orange(3)</td>
    <td>Common ground</td>
    <td>GRND of LightSystem</td>
  </tr>
  <tr>
    <td>L1</td>
    <td>32</td>
    <td>12</td>
    <td>Green(3)</td>
    <td>I/O Output</td>
    <td>Light 1</td>
  </tr>
  <tr>
    <td>L2</td>
    <td>33</td>
    <td>13</td>
    <td>Yellow(3)</td>
    <td>I/O Output</td>
    <td>Light 2</td>
  </tr>
  <tr>
    <td>L3</td>
    <td>36</td>
    <td>16</td>
    <td>Brown(3)</td>
    <td>I/O Output</td>
    <td>Light 3</td>
  </tr>
</table>

### Circuit Diagram

Displaying latest version of circuit diagram.

![](circuit_diagrams/complete-circuit.png)
