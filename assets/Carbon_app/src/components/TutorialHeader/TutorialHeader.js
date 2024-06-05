'use client';

import {
  Header,
  HeaderContainer,
  HeaderName,
  HeaderNavigation,
  HeaderMenuButton,
  HeaderMenuItem,
  HeaderGlobalBar,
  HeaderGlobalAction,
  SkipToContent,
  SideNav,
  SideNavItems,
  HeaderSideNavItems,
} from '@carbon/react';
import { Switcher, Notification, UserAvatar } from '@carbon/icons-react';

import Link from 'next/link';

const TutorialHeader = () => (
  <HeaderContainer
    render={({ isSideNavExpanded, onClickSideNavExpand }) => (
      <Header aria-label="Carbon Tutorial">
        <SkipToContent />
        <HeaderMenuButton
          aria-label="Open menu"
          onClick={onClickSideNavExpand}
          isActive={isSideNavExpanded}
        />
        <Link href="/" passHref legacyBehavior>
          <HeaderName prefix="IBM">Sentibot</HeaderName>
        </Link>
        <HeaderNavigation aria-label="Carbon Tutorial">
          <Link
            href="https://github.com/ibm-client-engineering/solution-sentibot"
            passHref
            legacyBehavior
          >
            <HeaderMenuItem>Repository</HeaderMenuItem>
          </Link>
        </HeaderNavigation>
        <HeaderGlobalBar>
          <HeaderGlobalAction
            aria-label="User Avatar"
            tooltipAlignment="left"
            className="action-icons"
          >
            <UserAvatar size={20} />
          </HeaderGlobalAction>
        </HeaderGlobalBar>
      </Header>
    )}
  />
);

export default TutorialHeader;
