import Head from 'next/head';
import styles from '../styles/Home.module.css';
import AuthContext from '../contexts/AuthContext';
import { useRouter } from 'next/router';
import { useEffect } from 'react';




export default function Home() {

  const router = useRouter();

  useEffect(() => {
    // Redirect to /removebg
    router.push('/removebg');
  }, []);

  return null;
}
