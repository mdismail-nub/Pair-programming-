import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Learn from "./pages/Learn";
import Challenges from "./pages/Challenges";
import Dashboard from "./pages/Dashboard";
import Navbar from "./components/Navbar";

export default function App(){return <BrowserRouter><div className='bg-bg text-textPrimary min-h-screen'><Navbar/><Routes><Route path='/' element={<Home/>}/><Route path='/learn' element={<Learn/>}/><Route path='/challenges' element={<Challenges/>}/><Route path='/dashboard' element={<Dashboard/>}/></Routes></div></BrowserRouter>}
