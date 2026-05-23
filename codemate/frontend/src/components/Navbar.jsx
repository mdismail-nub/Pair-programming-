import { Link } from "react-router-dom";
export default function Navbar(){return <nav className='p-4 border-b border-borderc flex gap-4'><Link to='/'>CodeMate</Link><Link to='/learn'>Learn</Link><Link to='/challenges'>Challenges</Link><Link to='/dashboard'>Dashboard</Link></nav>}
