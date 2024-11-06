"use client"
import { UserButton } from '@clerk/nextjs'
import Image from 'next/image'
import { usePathname } from 'next/navigation'
import Link from 'next/link'
import React, { useEffect } from 'react'
import 'react-toastify/dist/ReactToastify.css';


function Header() {
  const path = usePathname();

  useEffect(() => {
    console.log(path)
  }, [path])

  const workspaceKey = process.env.NEXT_PUBLIC_SUPRSEND_WORKSPACE_KEY || '';
  const subscriberId = process.env.NEXT_PUBLIC_SUPRSEND_SUBSCRIBER_ID || '';
  const distinctId = process.env.NEXT_PUBLIC_SUPRSEND_DISTINCT_ID || '';

  return (
    <div>
      <div className='flex p-4 items-center justify-between bg-secondary shadow-small'>
        <Image src={'/logo.svg'} width={160} height={100} alt='logo'/>
        <ul className='hidden md:flex gap-6'>
          <li className={`hover:text-primary hover:font-bold transition-all cursor-pointer
            ${path==='/dashboard' && 'text-primary font-bold'}
            `}>
            <Link href="/dashboard">Dashboard</Link>
          </li>

          <li className={`hover:text-primary hover:font-bold transition-all cursor-pointer
            ${path==='/' && 'text-primary font-bold'}
            `}>
            <Link href="/">Home</Link>
          </li>
        </ul>
        <UserButton/>
      </div>
    </div>
  )
}

export default Header
